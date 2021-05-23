from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.
# from sklearn.externals import joblib

import joblib
import models
import pickle
import models

# pickle.dump(open('./models/rffile.pkl', 'wb'))

reloadmodel=joblib.load('./models/rffilef.pkl')
reloaddrug=joblib.load('./models/lrfile.pkl')

age=""
sex=""
blood_pressure=""
cholesterol=""
kNa=""

def index(request):
    context={'a':'hello world'}
    return render(request,'index.html',context)

def drug(age,sex,blood_pressure,cholesterol,kNa):
    age_ztot=0
    age_ttof=0
    age_ftofi=0
    age_fitosi=0
    age_six=0
    sex_m=0
    sex_f=0
    bp_h=0
    bp_l=0
    bp_n=0
    chol_h=0
    chol_n=0
    k_1=0
    k_2=0
    k_3=0
    k_4=0
    k_5=0
    k_6=0
    if int(age)<= 30:
        age_ztot=1
    if int(age) > 30 and int(age) <= 40:
        age_ttof=1 
    if int(age) > 40 and int(age) <= 50:
        age_ftofi=1
    if int(age) > 50 and int(age) <= 60:
        age_fitosi=1
    if int(age) > 60:
        age_six=1
    if int(sex)==0:
        sex_m=1
    if int(sex)==1:
        sex_f=1
    if int(blood_pressure)<=90:
        bp_l=1
    if int(blood_pressure)>90 and int(blood_pressure)<=120:
        bp_n=1
    if int(blood_pressure)>120:
        bp_h=1
    if int(cholesterol)<=200:
        chol_n=1
    if int(cholesterol)>200:
        chol_h=1
    if float(kNa) <= 10:
        k_6=1
    if float(kNa) > 10 and float(kNa)  <= 15:
        k_1=1
    if float(kNa)  > 15 and float(kNa)  <= 20:
        k_2=1
    if float(kNa) > 20 and float(kNa)  <= 25:
        k_3=1
    if float(kNa)  > 25 and float(kNa)  <= 30:
        k_4=1
    if float(kNa)  > 30:
        k_5=1 
    temp=[[age_ztot,age_ttof,age_ftofi,age_fitosi,age_six,sex_f,sex_m,bp_h,bp_l,bp_n,chol_h,chol_n,k_1,k_2,k_3,k_4,k_5,k_6]]
    drugs=reloaddrug.predict(temp)
    if drugs[0]=="drugX":
        resultdrug="X"
    if drugs[0]=="DrugY":
        resultdrug="Y"
    if drugs[0]=="drugA":
        resultdrug="A"
    if drugs[0]=="drugB":
        resultdrug="B"
    if drugs[0]=="drugC":
        resultdrug="C"
    return resultdrug
       
def predictHDisease(request):
    print(request)
    ans=-1
    if request.method == 'POST':
       temp=[[]]
       age=request.POST.get('age')
       sex=request.POST.get('sex')
       chest_pain_type=request.POST.get('cp')
       blood_pressure=request.POST.get('bp')
       cholesterol=request.POST.get('chol')
       fasting_bloods_lvl=request.POST.get('fbs')
       ECG_results=request.POST.get('ecg')
       max_heart_rates=request.POST.get('maxhr')
       anigma=request.POST.get('EIA')
       ST_depression=request.POST.get('ST')
       slope_ST=request.POST.get('slopest')
       fluoro=request.POST.get('nov')
       thallium=request.POST.get('thal')
       kNa=request.POST.get('kna')
       temp=[[age,sex,chest_pain_type,blood_pressure,cholesterol,fasting_bloods_lvl,ECG_results,max_heart_rates,anigma,ST_depression,slope_ST,fluoro,thallium]]
       
       print(temp)
       predictvalue=reloadmodel.predict(temp)
       print(predictvalue[0])
       ans=predictvalue[0]

       recommendeddrug=drug(age,sex,blood_pressure,cholesterol,kNa)
       print(recommendeddrug)
       t=[[0,0,0,1,0,1,0,0,1,0,1,0,1,0,0,0,0,0]]
       drugs1=reloaddrug.predict(t)
       print(drugs1[0])
       msg="Consult a Doctor for medical advice"
       if recommendeddrug=="X":  
              description="Sodium to potassium levels is low in blood"
              drg="Consume potassium rich foods like beet greens, yams, white beans, clams, white potatoes, sweet potatoes, avocado, pinto beans and bananas."
              drg2="Drink a plenty of water"
       if recommendeddrug=="Y":
              description="Sodium to potassium levels is high in blood"
              drg="Sodium polystyrene sulfonate (Kayexalate)"
              drg2="Albuterol"
       if recommendeddrug=="A" :
               description="Blood Pressure high"
               drg="Bumetanide"
               drg2="Indapamide"
       if recommendeddrug=="B":
              description="Blood pressure high"
              drg="Esmolol"
              drg2="Benazepril hydrochloride"
       if recommendeddrug=="C":
              description="blood pressure Low"
              drg="fludrocortisone"
              drg2="midodrine"
       if ans==0:
          print("heart disease detected")
          result="WARNING!!! HEART DISEASE DETECTED"
          context ={'result':result,'description':description,'drg':drg,'drg2':drg2,'msg':msg}
        
        
        
        

       elif ans==1:
          print("heart disease not detected")
          result="HEART DISEASE NIL"
          context ={'result':result}
        
        
    return render(request,'index.html',context)