from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import sklearn
from geopy.geocoders import Nominatim
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
import pickle


#IMPORTING finalDATA.py 
import getData as fD

def countyFrame(CNTY) :
    data = {
        'CNTY NAME' : CNTY['CTNY'],
        'AGE RANGE' : CNTY['AGE RANGE'],
        'TOT POP BY AGE GROUP' : CNTY['TPOP PA PCN'],
        'CASES BY AGE GROUP' : CNTY['Number of Cases Per Age Range'],
        'MOBILITY TOTAL' : CNTY['MOBILITY TOTAL']
    }

    df = pd.DataFrame(data)
    df['PRECENT CASES BY AGE GROUP'] = (df['CASES BY AGE GROUP'] / df['TOT POP BY AGE GROUP'])*100

    #OUTBREAK THRESHOLD - can be described as 1 / Log(R0) -- R0 is the Basic Repoduction number, i.e. the number of people infected by one case
    #R0 number as of April 7, 2020 reported as 2.2 - 2.7 (2.4)
    outbreak_threshold = 1 / (math.log(5.7))
    mob_tot = data['MOBILITY TOTAL']
    df['IsOutbreak'] = df['PRECENT CASES BY AGE GROUP'] >= outbreak_threshold

    return df


#BUIDLING TESTING DATA SET

frames = []


with open('frames.pickle', 'rb') as f:
    frames = pickle.load(f)

df2 = pd.concat(frames)
df2.reset_index(drop=True, inplace=True)
#print(df2.to_string())

#Normalizing Mobility
prenormalized_mob = df2['MOBILITY TOTAL']
normalize_mob = df2['MOBILITY TOTAL']
df2 = df2.drop(['MOBILITY TOTAL'], axis=1 )
min_max_scaler = sklearn.preprocessing.MinMaxScaler()
normalize_mob = normalize_mob.to_numpy()
normalize_mob = normalize_mob.reshape(-1, 1)
mob_scaled = min_max_scaler.fit_transform(normalize_mob)
mob_scaled = pd.DataFrame(mob_scaled)
df2 = df2.join(mob_scaled)
df2.columns = ['CNTY NAME','AGE RANGE','TOT POP BY AGE GROUP', 'CASES BY AGE GROUP','PRECENT CASES BY AGE GROUP','IsOutbreak', 'Mobility Total']
df2 = df2.fillna(0)

df2['PRECENT CASES BY AGE GROUP'].loc[(df2['Mobility Total'] > .7)] = df2['PRECENT CASES BY AGE GROUP'] / .9
df2['IsOutbreak'].loc[(df2['PRECENT CASES BY AGE GROUP'] > (1 / (math.log(5.7))))] = True

#CLASSIFYING TESTING AND TRANING DATA
traing_data = df2.head(n=2000)
testing_data = df2.tail(n=1000)


#Creating model X and Y from traning
ids_training = traing_data[['CNTY NAME', 'AGE RANGE', 'PRECENT CASES BY AGE GROUP', 'Mobility Total']]
y = traing_data['IsOutbreak']
x = traing_data.drop(['CNTY NAME', 'AGE RANGE', 'IsOutbreak'], axis=1)
#modeling
model = LogisticRegression(random_state=42)
model.fit(x, y)


#GETTING TRAINING DATA AND COMPLINING INTO ONE DF
outbreak_prob = pd.DataFrame(model.predict_proba(x), columns=['Prob Not Outbreak', 'Predicted Prob Outbreak']) 
traing_result = ids_training.join(outbreak_prob)

#TESTING DATA
ids_testing = testing_data[['CNTY NAME', 'AGE RANGE', 'PRECENT CASES BY AGE GROUP', 'Mobility Total']]
testing_data = testing_data.drop(['CNTY NAME', 'AGE RANGE', 'IsOutbreak'], axis=1)
ids_testing.reset_index(drop=True, inplace=True)
testing_result = pd.DataFrame(model.predict_proba(testing_data), columns=['Prob Not Outbreak', 'Predicted Prob Outbreak'])
testing_result = ids_testing.join(testing_result)




#USER INPUT SECTION
def userInput(age, cnty, state) :
    try :
        cntyObj = 0

        for obj in frames :
            if cnty in obj.get('CNTY NAME')[0] and state in obj.get('CNTY NAME')[0]:
                cntyObj = obj
            else :
                continue

        #NORMALIZING MOBILITY

        normalize_mob1 = pd.concat([prenormalized_mob, cntyObj.get('MOBILITY TOTAL')], axis = 0)
        normalize_mob1 = normalize_mob1.to_numpy()
        normalize_mob1 = normalize_mob1.reshape(-1, 1)
        mob_scaled1 = min_max_scaler.fit_transform(normalize_mob1)
        mob_scaled1 = pd.DataFrame(mob_scaled1)
        mob_scaled1 = mob_scaled1.fillna(0)
        mob_scaled1 = mob_scaled1.tail(n=18)
        mob_scaled1.reset_index(drop=True, inplace=True)


        cntyObj = pd.DataFrame(cntyObj)
        cntyObj['MOBILITY TOTAL'] = mob_scaled1

        #cntyObj['PRECENT CASES BY AGE GROUP'].loc[(cntyObj['MOBILITY TOTAL'] > .7)] = cntyObj['PRECENT CASES BY AGE GROUP'] / .9

        ids = cntyObj[['CNTY NAME', 'AGE RANGE', 'PRECENT CASES BY AGE GROUP', 'MOBILITY TOTAL']]
        unique_data = cntyObj.drop(['CNTY NAME', 'AGE RANGE', 'IsOutbreak'], axis=1)
        user_results = pd.DataFrame(model.predict_proba(unique_data), columns=['Prob Not Outbreak', 'Predicted Prob Outbreak'])
        final_df = ids.join(user_results)

        final_df.columns = ['Location','Age Range', 'Percent of Cases By Age Group','Mobility Score', 'Predicted Probability of Not Outbreak', 'Predicted Probability of Outbreak']

        ageList = [(0,4), (5,9), (10,14), (15,19), (20,24), (25,29), (30, 34), (35,39), (40, 44), (45,49), (50,54),(55,59), (60,64), (65,69), (70,74), (75,79), (80,84), (85, 999)]

        indexOfAge = 0

        for index, i in enumerate(ageList):
            if i[0] <= age and age <= i[1]:
                indexOfAge = index

        ageCol = final_df.iloc[indexOfAge]

        return ([final_df.to_html(classes='data')], final_df.columns.values, ageCol)

    except :
        return "error"

userInput(12, 'Los Angeles', 'California')