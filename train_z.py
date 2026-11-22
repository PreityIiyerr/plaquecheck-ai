"""Train CAD research models from Z-Alizadeh Sani workbook. No clinical decision labels."""
import argparse,json,pathlib
import pandas as pd
from sklearn.model_selection import train_test_split
from train_uci import fit,score,metrics
CORE=['age','male','dm','htn','sbp','dyspnea']
EXT=CORE+['qwave','bbb','ef','rwma']
def prepare(path):
    d=pd.read_excel(path).drop_duplicates(); x=pd.DataFrame(index=d.index)
    for k,c in [('age','Age'),('dm','DM'),('htn','HTN'),('sbp','BP'),('ef','EF-TTE'),('qwave','Q Wave')]: x[k]=pd.to_numeric(d[c],errors='coerce')
    x['male']=d.Sex.map({'Male':1,'Fmale':0,'Female':0}); x['dyspnea']=d.Dyspnea.map({'Y':1,'N':0}); x['bbb']=d.BBB.map({'N':0,'LBBB':1,'RBBB':1}); x['rwma']=d['Region RWMA'].map({0:0,1:1,2:1,3:1,4:1}); x['y']=d.Cath.map({'Cad':1,'Normal':0});return x

def train(x,f,name):
    d=x.dropna(subset=f+['y']);dev,te=train_test_split(d,test_size=.2,stratify=d.y,random_state=42);tr,ca=train_test_split(dev,test_size=.25,stratify=dev.y,random_state=43); obj=fit(tr,ca,f);s,m,c=obj
    met=metrics(te.y,score(obj,te,f))|{'n_train':len(tr),'n_calibration':len(ca),'n_eligible':len(d)}
    return {'schema':'plaquecheck-v1','name':name,'target':'obstructive_cad','source':'Z-Alizadeh Sani, UCI 412; Cath Cad vs Normal, angiography-selected cohort','features':f,'median':s.mean_.tolist(),'mean':s.mean_.tolist(),'scale':s.scale_.tolist(),'coef':m.coef_[0].tolist(),'intercept':float(m.intercept_[0]),'calibration_coef':float(c.coef_[0,0]),'calibration_intercept':float(c.intercept_[0]),'metrics':met,'age_min':int(d.age.min()),'age_max':int(d.age.max()),'limitations':['Single-centre historical referral cohort; only 303 records.','No angiography decision labels, no deferred cohort, no clinical rule-out threshold.','Only confirmed inputs; no imputation; binary BBB and RWMA.','No external or prospective validation.']}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('--out',default='z_models.json');a=p.parse_args();x=prepare(a.data);models=[train(x,CORE,'Z-Alizadeh clinical model'),train(x,EXT,'Z-Alizadeh clinical + ECG/echo model')];pathlib.Path(a.out).write_text(json.dumps(models,indent=2));print(json.dumps([{k:m[k] for k in ['name','metrics','age_min','age_max']} for m in models],indent=2))
