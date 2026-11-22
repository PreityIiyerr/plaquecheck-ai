"""Train two research CAD models from the supplied UCI CSV; never an angiography decision score."""
import argparse,json,pathlib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,brier_score_loss,confusion_matrix

BASE=['age','male','sbp','cp_typical','cp_atypical','cp_nonanginal']
EXT=BASE+['chol','fbs','rest_st','rest_lvh']
def prepare(path):
    d=pd.read_csv(path)
    d=d.drop_duplicates(subset=[c for c in d if c!='id']).copy()
    x=pd.DataFrame(index=d.index)
    x['age']=pd.to_numeric(d.age,errors='coerce');x['male']=d.sex.map({'Female':0,'Male':1});x['sbp']=pd.to_numeric(d.trestbps,errors='coerce').replace(0,np.nan)
    for key,category in [('cp_typical','typical angina'),('cp_atypical','atypical angina'),('cp_nonanginal','non-anginal')]:
        x[key]=np.where(d.cp.isin(['typical angina','atypical angina','non-anginal','asymptomatic']), (d.cp==category).astype(int),np.nan)
    x['chol']=pd.to_numeric(d.chol,errors='coerce').replace(0,np.nan);x['fbs']=d.fbs.map({True:1,False:0,'True':1,'False':0})
    for key,category in [('rest_st','st-t abnormality'),('rest_lvh','lv hypertrophy')]:
        x[key]=np.where(d.restecg.isin(['normal','st-t abnormality','lv hypertrophy']),(d.restecg==category).astype(int),np.nan)
    x['site']=d.dataset;x['y']=(d.num>0).astype(int)
    return x

def fit(train,cal,features):
    s=StandardScaler().fit(train[features]);m=LogisticRegression(max_iter=2000).fit(s.transform(train[features]),train.y)
    c=LogisticRegression(max_iter=2000).fit(m.decision_function(s.transform(cal[features])).reshape(-1,1),cal.y)
    return s,m,c

def score(fitobj,d,features):
    s,m,c=fitobj
    return c.predict_proba(m.decision_function(s.transform(d[features])).reshape(-1,1))[:,1]

def metrics(y,p):
    tn,fp,fn,tp=confusion_matrix(y,p>=.5,labels=[0,1]).ravel()
    return {k:round(float(v),4) for k,v in {'auc':roc_auc_score(y,p),'brier':brier_score_loss(y,p),'accuracy':(tn+tp)/len(y),'sensitivity_at_0_5':tp/(tp+fn),'specificity_at_0_5':tn/(tn+fp),'prevalence':np.mean(y)}.items()}|{'n_test':len(y),'tn':int(tn),'fp':int(fp),'fn':int(fn),'tp':int(tp)}

def train(x,features,name):
    d=x.dropna(subset=features).copy();d=d[d.age.between(30,77)]
    dev,te=train_test_split(d,test_size=.2,stratify=d.y,random_state=42)
    tr,ca=train_test_split(dev,test_size=.25,stratify=dev.y,random_state=43)
    obj=fit(tr,ca,features);s,m,c=obj
    met=metrics(te.y,score(obj,te,features))|{'n_train':len(tr),'n_calibration':len(ca),'n_eligible':len(d)}
    site_results={}
    for site in sorted(d.site.unique()):
        held=d[d.site==site];other=d[d.site!=site]
        if held.y.nunique()!=2 or len(held)<15:continue
        t,cal=train_test_split(other,test_size=.25,stratify=other.y,random_state=43)
        site_results[site]=metrics(held.y,score(fit(t,cal,features),held,features))
    return {'schema':'plaquecheck-v1','name':name,'target':'obstructive_cad','source':'User-supplied UCI Heart Disease CSV; num > 0','features':features,'median':s.mean_.tolist(),'mean':s.mean_.tolist(),'scale':s.scale_.tolist(),'coef':m.coef_[0].tolist(),'intercept':float(m.intercept_[0]),'calibration_coef':float(c.coef_[0,0]),'calibration_intercept':float(c.intercept_[0]),'metrics':met,'site_holdout':site_results,'age_min':30,'age_max':77,'limitations':['Complete cases only; geographic and historical referral-cohort selection bias.','0 values for BP and cholesterol treated as missing.','No ca (fluoroscopy), thal, stress measures, site or ID in model.','Threshold 0.5 for evaluation only; not a care threshold.','No appropriateness labels; no clinical decision confidence.']}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('--out',default='uci_models.json');a=p.parse_args();x=prepare(a.data);models=[train(x,BASE,'UCI basic clinical model'),train(x,EXT,'UCI expanded clinical model')];pathlib.Path(a.out).write_text(json.dumps(models,indent=2));print(json.dumps([{k:m[k] for k in ['name','metrics','site_holdout']} for m in models],indent=2))
