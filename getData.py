import urllib.request
import json
import heapq
import pandas as pd
import math
import pickle

url = "https://coronavirus.m.pipedream.net/"

# open json
with urllib.request.urlopen(url) as url:
    data = json.loads(url.read().decode())

caseInfo = data['rawData']


# init locations countries, and states
locations = []

# loop through data
for i in range(len(caseInfo)):

    # get current place
    place = caseInfo[i]

    # if there are any cases
    if place['Country_Region'] == 'US':
        locations.append({'place': place['Combined_Key'], 'cases': place['Confirmed'], 'lat': place['Lat'], 'long': place['Long_'], 'state': place['Province_State']})

# with open('cityList.pickle', 'wb') as f:
#     pickle.dump(locations, f)

# with open('cityList.pickle', 'rb') as f:
#     locations = pickle.load(f)

def nearest(pointA):
    # function to calc distance
    def calc_euclidean_distance(point_a, point_b):
        return math.sqrt(math.pow(point_a[0] - point_b[0], 2) + math.pow(point_a[1] - point_b[1], 2))

    # init heap
    heap = []

    # loop through all locations to find closest
    for index, place in enumerate(locations):
        # if if its not empty
        if (place['long'] != "") and (place['lat'] != ""):

            longi = float(place['long'])
            lat = float(place['lat'])

            pointB = [longi, lat]
            d = [calc_euclidean_distance(pointA, pointB), index, place]

            heapq.heappush(heap, d)
    nearest = heapq.heappop(heap)[1]

    return(locations[nearest])

"""## Calc Probabilities"""

def prob(cityObj):
    # get string name
    strngName = cityObj['place'].split(", ")

    mobilityData = ('https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/google_reports/mobility_report_US.csv')

    dfMobility = pd.read_csv(mobilityData)
    dfMobility['date'] = pd.to_datetime(dfMobility['date'])
    dfMobility.fillna(0, inplace=True)
    try:
        df3 = dfMobility[dfMobility['state'].str.contains(strngName[1]) & dfMobility['county'].str.contains(strngName[0])]
        total = df3.tail(n=7)
        total = total.sum(axis=1, skipna=True)
        mobilityTotal = total.mean(axis=0)

    except:
        print('ERROR FINDING MOBILITY', cityObj)
        mobilityTotal = 0
        pass

    # read sex by county and returns a male to female distribution
    dfSDist = pd.read_csv('data/output.csv')
    df4 = dfSDist[dfSDist['STNAME'].str.contains(strngName[1]) & dfSDist['CTYNAME'].str.contains(strngName[0])]

    #Adding all columns
    tot_pop = df4['TOT_POP']
    tot_pop = tot_pop[tot_pop.idxmax()]

    #MEAN DISTRIBUTION OF AGE BY COUNTY
    age_groups = ['Total', '0:4', '5:9',  '10:14', '15:19',  '20:24', '25:29', '30:34', '35:39', '40:44', '45:49', '50:54', '55:59', '60:64', '65:69', '70:74', '75:79', '80:84', '85+']
    age_tot = []

    for row in df4['TOT_POP'] :
        age_tot.append(row)

    tot_pop = age_tot[0]
    age_groups = age_groups[1:]
    age_tot = age_tot[1:]

    #CASES PER AGE RANGE
    casesT = cityObj['cases']
    casesP = int(casesT) / tot_pop
    ageG_cases = []

    for row in age_tot :
        ageG_cases.append(math.floor(row * casesP))

    return {'CTNY' : cityObj['place'], 'STN' : cityObj['state'], 'TOT POP': tot_pop, 'TOT CASES': cityObj['cases'], 'AGE RANGE' : age_groups, 'TPOP PA PCN' : age_tot, 'PRECENT OF POP INFECTED' : casesP, 'Number of Cases Per Age Range' : ageG_cases, 'MOBILITY TOTAL' : mobilityTotal}