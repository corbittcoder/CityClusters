import pandas as pd
import numpy as np
import sys
pd.options.mode.chained_assignment = None
import plot

MILES_PER_LAT = 69
MILES_PER_LNG = 53
MILES_PER_HOUR = 30
def knn(places, numGroups):
    numTimes = 5
    prevPlaces = pd.DataFrame()
    while not places.equals(prevPlaces) and numTimes > 0:
        prevPlaces = places.copy()

        #determine distance from each cluster
        for index, row in places.iterrows():
            # distances = np.zeros(numGroups)
            #Get 5 closest points to current point
            places['Distances'] = abs(places.Lng - row.Lng) + abs(places.Lat - row.Lat)
            colors = places.sort_values(by=['Distances']).iloc[0:50]['Color'].unique()[0:3]
            distances = pd.Series(data = np.zeros(len(colors)), index = colors)
            mindex = colors[0] #index of minimum distance
            for i in colors:

                #get all points of that color
                color = places[places.Color == i]

                #Calculate distance from all points
                color.Lng -= row['Lng']
                color.Lat -= row['Lat']
                color['Distance'] = (abs(color.Lng) * MILES_PER_LNG + abs(color.Lat) * MILES_PER_LAT)
                    #color.assign(Distance=lambda color: (color.Lng ** 2 + color.Lat ** 2) ** .5)

                # distances[i] = color.Distance.min(axis=0)
                distances[i] = (color.Distance.sum() / MILES_PER_HOUR / len(color) * row.NumVisits) + (color.Hours.sum() / 10) #don't want the cells to get too big

                if row.Color == i:
                    distances[i] -= row.Hours
                if distances[i] < distances[mindex]:
                    mindex = i
            places.loc[index, 'Color'] = mindex
        numTimes -= 1
        print(numTimes)
    return places

def main(places, name, numGroups, api):
    #Group by zip code
    zips = places.drop_duplicates(subset=['ShortZip'])

    #Sort by zip code groups to get rough groups
    # zips['Hours'] = zips.ShortZip.replace(hours)
    zips['Hours'] = np.zeros(len(zips))
    zips['Color'] = np.random.randint(0, numGroups, zips.shape[0])
    zips['NumVisits'] = np.ones(len(zips))
    zips = knn(zips, numGroups)

    #Assign groups to full dataframe
    places['Color'] = places.ShortZip.replace(zips.set_index('ShortZip')['Color'])
    plot.plot(places, name, api) #compare pre- to post-sorting
    # #now measure with just distance
    # distanceOnly = places.copy()
    # distanceOnly['Hours'] = np.zeros(len(places))
    # distanceOnly = knn(distanceOnly, numGroups)
    #Now get exact groups starting from rough basis
    places = knn(places, numGroups)

    #Calculate man-hours for each group
    hours = places.groupby(['Color'])['Hours'].sum()
    for color, totalHours in hours.items():
        group = places[places.Color == color]
        group.Lat -= group['Lat'].mean()
        group.Lng -= group['Lng'].mean()
        group['Distance'] = (abs(group.Lng) * MILES_PER_LNG + abs(group.Lat) * MILES_PER_LAT) * group.NumVisits
        hours[color] = group.Distance.sum() / MILES_PER_HOUR + totalHours

    #plot data points on map
    try:
        places.to_csv('files\\' + name + '_results.csv', index = False)
        hours.to_csv('files\\' + name + '_hours.csv', index=False)
    except:
        print("Couldn't save")
    plot.plot(places, name, api)

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

