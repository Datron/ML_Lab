# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 10:39:40 2018

@author: kartik
"""
import bayespy as bp
import numpy as np
import csv
from colorama import init
from colorama import Fore,Back,Style

init()
# define parameter enum values
# age
ageEnum = {'SuperSeniorCitizen':0,'SeniorCitizen':1,'MiddleAged':2,'Youth':3,'Teen':4}
# gender
genderEnum = {'Male':0,'Female':1}
#family history
familyHistoryEnum = {'Yes':0,'No':1}

dietEnum = {'High':0,'Medium':1,'Low':2}

lifeStyleEnum = {'Athlete':0,'Active':1,'Moderate':2,'Sedetary':3}

cholesterolEnum = {'High':0,'BorderLine':1,'Normal':2}

heartDiseaseEnum = {'Yes':0,'No':1}

with open('heart_disease_data.csv') as csvfile:
    lines = csv.reader(csvfile)
    dataset = list(lines)
    data = []
    for x in dataset:
        data.append([ageEnum[x[0]],genderEnum[x[1]],familyHistoryEnum[x[2]],dietEnum[x[3]],lifeStyleEnum[x[4]],cholesterolEnum[x[5]],heartDiseaseEnum[x[6]]])
    data = np.array(data)
    N = len(data)

p_age = bp.nodes.Dirichlet(1.0*np.ones(5))
age = bp.nodes.Categorical(p_age,plates=(N,))
age.observe(data[:,0])

p_gender = bp.nodes.Dirichlet(1.0*np.ones(2))
gender = bp.nodes.Categorical(p_gender,plates = (N,))
gender.observe(data[:,1])

p_familyhistory = bp.nodes.Dirichlet(1.0*np.ones(2))
familyhistory = bp.nodes.Categorical(p_familyhistory,plates = (N,))
familyhistory.observe(data[:,2])

p_diet = bp.nodes.Dirichlet(1.0*np.ones(3))
diet = bp.nodes.Categorical(p_diet, plates=(N,))
diet.observe(data[:,3])

p_lifestyle = bp.nodes.Dirichlet(1.0*np.ones(4))
lifestyle = bp.nodes.Categorical(p_lifestyle, plates=(N,))
lifestyle.observe(data[:,4])

p_cholesterol = bp.nodes.Dirichlet(1.0*np.ones(3))
cholesterol = bp.nodes.Categorical(p_cholesterol, plates=(N,))
cholesterol.observe(data[:,5])

# prepare nodes and establish edges
#np.ones(2) -> HeartDisease has 2 options Yes/No
# plates(5,2,2,3,4,3) -. corresponds to options present for domain values
p_heartdisease = bp.nodes.Dirichlet(np.ones(2),plates=(5,2,2,3,4,3))
heartdisease = bp.nodes.MultiMixture([age,gender,familyhistory,diet,lifestyle,cholesterol],bp.nodes.Categorical,p_heartdisease)
heartdisease.observe(data[:,6])
p_heartdisease.update()

# sample test with hardcoded values
# print("Sample Probability")
#print("probability(HeartDisease|Age=SuperSeniorCitizen,Gender=Female,FamilyHistory=Yes,Diet=Medium,lifestyle=sedetary,cholesterol=High"))
#print(bp.nodes.MultiMixture([ageEnum['SuperSeniorCitizen'],genderEnum['Female'],familyHistoryEnum['Yes'],dietEnum['High'],lifeStyleEnum['Sedetary'],cholesterolEnum['High']],bp.nodes.Categorical,p_heartdisease).get_moments()[0][heartDiseaseEnum['Yes']])

#interactive test
m = 0
while m == 0:
    print("\n")
    res = bp.nodes.MultiMixture([int(input('Enter Age:'+str(ageEnum))),int(input('Enter Gender:'+str(genderEnum))),int(input('Enter Family History:'+str(familyHistoryEnum))),int(input('Enter diet:'+str(dietEnum))),int(input('Enter life style:'+str(lifeStyleEnum))),int(input('Enter cholesterol:'+str(cholesterolEnum)))],bp.nodes.Categorical,p_heartdisease).get_moments()[0][heartDiseaseEnum['Yes']]
    print('Probability(HeartDisease)='+str(res))
    #print(Style.RESET_ALL)
    m = int(input("Continue:0 exit:1"))

"""
Enter Age:{'SuperSeniorCitizen': 0, 'SeniorCitizen': 1, 'MiddleAged': 2, 'Youth': 3, 'Teen': 4}0

Enter Gender:{'Male': 0, 'Female': 1}1

Enter Family History:{'Yes': 0, 'No': 1}1

Enter diet:{'High': 0, 'Medium': 1, 'Low': 2}1

Enter life style:{'Athlete': 0, 'Active': 1, 'Moderate': 2, 'Sedetary': 3}0

Enter cholesterol:{'High': 0, 'BorderLine': 1, 'Normal': 2}2
Probability(HeartDisease)=0.5

Continue:0 exit:11
"""