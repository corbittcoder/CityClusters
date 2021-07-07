import pandas as pd
import gmplot
import numpy as np
import sys

def knn(places, name):
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'brown'] #colors of groups
    prevPlaces = pd.DataFrame()
    places['Color'] = np.random.randint(0, len(colors), places.shape[0])
    while not places.equals(prevPlaces):
        prevPlaces = places.copy()
        #determine distance from each cluster
        for index, row in places.iterrows():
            distances = np.zeros(len(colors))
            mindex = 0 #index of minimum distance
            for i in range(len(distances)):
                #get all points of that color
                color = places[places.Color == i]
                #Calculate distance from all points
                color.Lng -= row['Lng']
                color.Lat -= row['Lat']
                color = color.assign(Distance=lambda color: color.Lng ** 2 + color.Lat ** 2)
                # distances[i] = color.Distance.min(axis=0)
                distances[i] = color.Distance.sum() / (len(color) ** 0.5) #don't want the cells to get too big
                if distances[i] < distances[mindex]:
                    mindex = i
                if len(color) == 0:
                    mindex = i
            places.loc[index, 'Color'] = mindex

    #Name clusters
    # names = []
    # for i in range(len(colors)):
    #     cluster = places[places.Color == i]
    #     averageLocation = [cluster['Lat'].mean(), cluster['Lng'].mean()]
    #     cluster.Lat -= averageLocation[0]
    #     cluster.Lng -= averageLocation[1]
    #     cluster = cluster.assign(Distance=lambda cluster: cluster.Lng ** 2 + cluster.Lat ** 2)
    #     #find spot closest to the center
    #     names = names.append(cluster[cluster.Distance == cluster.Distance.min()].Name[0])


    #plot data points on map
    gmap = gmplot.GoogleMapPlotter.from_geocode(name + ", Florida", apikey='')
    for i in range(len(colors)):
        group = places[places.Color == i]
        gmap.scatter(group.Lat.tolist(), group.Lng.tolist(), color=colors[i])
    gmap.draw(r"C:\Users\scttc\PycharmProjects\CityClusters\\" + name + "_map.html")
    places.to_csv('files\\' + name + '_results.csv', index=False)

if __name__ == '__main__':
    name = ""
    if len(sys.argv) != 2:
            print('Usage: knn.py <CITY NAME>')
            exit(1)
    else:
            name = sys.argv[1]
    places = pd.read_csv(r"C:\Users\scttc\PycharmProjects\CityClusters\files\\" + name + "_values.csv")
    knn(places, name)

