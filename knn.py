import pandas as pd
import numpy as np
import sys

import plot

def knn(places, name, numGroups, api):
    pd.options.mode.chained_assignment = None
    CYCLES = 2
    # colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'brown'] #colors of groups
    # colors = colors[0, numGroups]
    prevPlaces = pd.DataFrame()
    places['Color'] = np.random.randint(0, numGroups, places.shape[0])
    while (CYCLES > 0): #not places.equals(prevPlaces)
        prevPlaces = places.copy()
        #determine distance from each cluster
        for index, row in places.iterrows():
            centers = pd.DataFrame(columns=['Color', 'Lat', 'Lng', 'Hours'])
            for i in range(len(numGroups)):
                #get all points of that color
                color = places[places.Color == i]
                lat = np.mean(color.Lat)
                lng = np.mean(color.Lng)
                hours = np.sum(color.Hours)
                centers.append(i, lat, lng, hours)
            distances = np.zeros(numGroups)
            mindex = 0 #index of minimum distance
            for color in centers:
                color.Lng *= 52 / 45 * row.NumVisits #conversion rate to hours of travel time
                color.Lat *= 69 / 45 * row.NumVisits #conversion rate to hours of travel time
                distance = color.Lng ** 2 + color.Lat ** 2 + color.Hours
                # distances[i] = color.Distance.min(axis=0)
                #TODO: does this line below have the opposite effect as intended?
                #distances[i] = color.Distance.sum() / (len(color) ** 0.5) #don't want the cells to get too big
                if distances[i] < distances[mindex]:
                    mindex = i
                if len(color) == 0:
                    mindex = i
            places.loc[index, 'Color'] = mindex
        print(CYCLES)
        CYCLES -= 1

    #Name clusters
    # names = []
    # for i in range(numGroups):
    #     cluster = places[places.Color == i]
    #     averageLocation = [cluster['Lat'].mean(), cluster['Lng'].mean()]
    #     cluster.Lat -= averageLocation[0]
    #     cluster.Lng -= averageLocation[1]
    #     cluster = cluster.assign(Distance=lambda cluster: cluster.Lng ** 2 + cluster.Lat ** 2)
    #     #find spot closest to the center
    #     names = names.append(cluster[cluster.Distance == cluster.Distance.min()].Name[0])


    #plot data points on map
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
    places = pd.read_csv(r"C:\Users\scttc\PycharmProjects\CityClusters\files\\" + name + "_values.csv")
    knn(places, name, numGroups, api)

