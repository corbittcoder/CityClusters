import pandas as pd
import gmplot
import numpy as np
import sys

def plot(places, name):
    #plot data points on map
    colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange'] #colors of groups
    gmap = gmplot.GoogleMapPlotter.from_geocode(name + ", Florida", apikey='')
    for i in range(len(colors)):
        group = places[places.Color == i]
        gmap.scatter(group.Lat.tolist(), group.Lng.tolist(), color=colors[i])
    gmap.draw(r"C:\Users\scttc\PycharmProjects\CityClusters\\" + name + "_map.html")

if __name__ == '__main__':
    name = ""
    if len(sys.argv) != 2:
            print('Usage: plot.py <CITY NAME>')
            exit(1)
    else:
            name = sys.argv[1]
    places = pd.read_csv(r"C:\Users\scttc\PycharmProjects\CityClusters\files\\" + name + "_results.csv")
    plot(places, name)

