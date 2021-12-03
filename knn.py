import pandas as pd
import numpy as np
import sys

import plot

def knn(places, numGroups):
    numTimes = 5
    prevPlaces = pd.DataFrame()
    while not places.equals(prevPlaces) and numTimes > 0:
        prevPlaces = places.copy()

        #determine distance from each cluster
        for index, row in places.iterrows():
            # distances = np.zeros(numGroups)
            mindex = 0 #index of minimum distance
            #Get 5 closest points to current point
            places['Distances'] = abs(places.Lng - row.Lng) + abs(places.Lat - row.Lat)
            colors = places.sort_values(by=['Distances']).iloc[0:5]['Color'].unique()
            distances = np.zeros(len(colors))
            for i in range(len(colors)):

                #get all points of that color
                color = places[places.Color == colors[i]]

                #Calculate distance from all points
                color.Lng -= row['Lng']
                color.Lat -= row['Lat']
                milesPerLat = 69
                milesPerLng = 53
                milesPerHour = 45
                color['Distance'] = (abs(color.Lng) * milesPerLng + abs(color.Lat) * milesPerLat) / milesPerHour
                    #color.assign(Distance=lambda color: (color.Lng ** 2 + color.Lat ** 2) ** .5)

                # distances[i] = color.Distance.min(axis=0)
                distances[i] = color.Distance.sum() / (len(color)) + color.Hours.sum() #don't want the cells to get too big

                if row.Color == i:
                    distances[i] -= row.Hours
                if distances[i] < distances[mindex]:
                    mindex = i
            places.loc[index, 'Color'] = colors[mindex]
        numTimes -= 1
    return places

def main(places, name, numGroups, api):
    #Group by zip code
    hours = places.groupby(['ShortZip'])['Hours'].sum()
    zips = places.drop_duplicates(subset=['ShortZip'])

    #Sort by zip code groups to get rough groups
    zips['Hours'] = zips.ShortZip.replace(hours)
    zips['Color'] = np.random.randint(0, numGroups, zips.shape[0])
    zips = knn(zips, numGroups)

    #Assign groups to full dataframe
    places['Color'] = places.ShortZip.replace(zips.set_index('ShortZip')['Color'])
    #Now get exact groups starting from rough basis
    places = knn(places, numGroups)

    #plot data points on map
    try:
        places.to_csv('files\\' + name + '_results.csv', index = False)
    except:
        print("Couldn't save")
    plot.plot(places, name, numGroups, api)

if __name__ == '__main__':
    api = ''
    name = ''
    numGroups = 0
    if len(sys.argv) != 4:
        print('Usage: knn.py <GOOGLE API KEY> <CITY NAME> <NUM GROUPS>')
        exit(1)
    else:
        api = sys.argv[1]
        name = sys.argv[2]
        try:
            numGroups = int(sys.argv[3])
        except:
            print('Usage: knn.py <GOOGLE API KEY> <CITY NAME> <NUM GROUPS>')
    places = pd.read_csv(r"files\\" + name + "_values.csv")
    main(places, name, numGroups, api)

