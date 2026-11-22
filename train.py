"""Research-only model trainer. No clinical deployment or recommendation."""
import argparse, json, pathlib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,brier_score_loss,balanced_accuracy_score

MAP={'Age':'age','Sex':'male','DM':'dm','HTN':'htn','DLP':'dyslipid','FH':'family','BP':'sbp','Dyspnea':'dyspnea','Q Wave':'qwave','EF-TTE':'ef','Typical Chest Pain':'typical','Atypical':'atypical'}
FEATURES=['age','male','dm','htn','dyslipid','smoke','family','sbp','dyspnea','qwave','bbb','ef','rwma','typical','atypical']
BINARY=set(FEATURES)-{'age','sbp','ef'}
def numeric(s):return pd.to_numeric(s,errors='coerce')
def binary(s):
    return s.astype(str).str.strip().str.lower().map({'1':1,'1.0':1,'0':0,'0.0':0,'yes':1,'no':0,'y':1,'n':0,'true':1,'false':0,'m':1,'male':1,'f':0,'female':0})
def load(path,target):
    path=pathlib.Path(path)
    if path.suffix.lower()=='.xlsx': d=pd.read_excel(path)
    else:d=pd.read_csv(path)
    d.columns=d.columns.str.strip()
    if target=='obstructive_cad' and 'Cath' in d.columns:
        y=d['Cath'].astype(str).str.strip().str.lower().map({'cad':1,'normal':0})
        x=pd.DataFrame(index=d.index)
        for orig,k in MAP.items():
            if orig in d:x[k]=binary(d[orig]) if k in BINARY else numeric(d[orig])
        if 'Current Smoker' in d and 'EX-Smoker' in d:
            s1,s2=binary(d['Current Smoker']),binary(d['EX-Smoker']);x['smoke']=np.where((s1==1)|(s2==1),1,np.where((s1==0)&(s2==0),0,np.nan))
        # BBB/RWMA omitted: coding conventions vary by file version.
        source='UCI Z-Alizadeh Sani; Cath label, angiography-selected cohort'
    else:
        if target not in d:raise ValueError(f'Missing target column {target}')
        if target=='ica_appropriate':
            if 'stable_eligible' not in d:raise ValueError('Decision dataset requires stable_eligible=1 for clinician-confirmed eligible stable cases.')
            d=d[binary(d.stable_eligible)==1].copy()
        y=binary(d[target]);x=pd.DataFrame({k:(binary(d[k]) if k in BINARY else numeric(d[k])) for k in FEATURES if k in d},index=d.index)
        source='User-supplied research cohort; provenance and labels must be independently verified'
    if not len(x.columns):raise ValueError('No recognized feature columns found')
    if y.isna().any():raise ValueError('Unrecognized or missing outcome labels. Resolve explicitly before training.')
    # Remove duplicates by exact feature+target identity before splitting; no patient IDs used.
    j=x.assign(__y=y).drop_duplicates();y=j.pop('__y').astype(int);x=j
    if 'age' in x:
        valid=x.age.between(30,80);x=x.loc[valid];y=y.loc[valid]
    x=x.dropna(axis=1,how='all');x=x.loc[:,x.nunique(dropna=True)>1]
    if not len(x.columns):raise ValueError('No nonconstant usable features')
    if len(x)<100 or y.value_counts().min()<25:raise ValueError('Need at least 100 rows and 25 per outcome class for this exploratory split (not a clinical sample-size justification).')
    return x,y,source

def train(path,target,out):
    x,y,source=load(path,target)
    # 60% fit, 20% calibration, 20% untouched internal test.
    x_dev,x_te,y_dev,y_te=train_test_split(x,y,test_size=.2,stratify=y,random_state=42)
    x_tr,x_ca,y_tr,y_ca=train_test_split(x_dev,y_dev,test_size=.25,stratify=y_dev,random_state=43)
    usable=x_tr.columns[x_tr.notna().any()];x_tr=x_tr[usable];x_ca=x_ca[usable];x_te=x_te[usable]
    imp=SimpleImputer(strategy='median').fit(x_tr);scale=StandardScaler().fit(imp.transform(x_tr))
    def transform(v):return scale.transform(imp.transform(v))
    model=LogisticRegression(max_iter=1000).fit(transform(x_tr),y_tr)
    cal=LogisticRegression(max_iter=1000).fit(model.decision_function(transform(x_ca)).reshape(-1,1),y_ca)
    p=cal.predict_proba(model.decision_function(transform(x_te)).reshape(-1,1))[:,1]
    result={'schema':'plaquecheck-v1','target':target,'source':source,'features':list(usable),'median':imp.statistics_.tolist(),'mean':scale.mean_.tolist(),'scale':scale.scale_.tolist(),'coef':model.coef_[0].tolist(),'intercept':float(model.intercept_[0]),'calibration_coef':float(cal.coef_[0,0]),'calibration_intercept':float(cal.intercept_[0]),'metrics':{'auc':round(float(roc_auc_score(y_te,p)),3),'brier':round(float(brier_score_loss(y_te,p)),3),'balanced_accuracy_at_0_5':round(float(balanced_accuracy_score(y_te,p>=.5)),3),'n_train':len(x_tr),'n_calibration':len(x_ca),'n_test':len(x_te)},'limitations':['Single random internal split; no external or prospective validation.','No clinical cutoffs established.','Browser withholds prediction if any selected input is missing. Test metrics may include median-imputed test rows and are not directly transferable to complete-case browser use.','Dataset selection, repeated-patient records, site/time shifts, outcome adjudication and calibration require independent review.']}
    pathlib.Path(out).write_text(json.dumps(result,indent=2));print(json.dumps(result['metrics'],indent=2));print('Saved research model:',out)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('data',help='UCI .xlsx or standardized .csv');a.add_argument('--target',choices=['obstructive_cad','ica_appropriate'],default='obstructive_cad');a.add_argument('--out',default='research_model.json');args=a.parse_args();train(args.data,args.target,args.out)
