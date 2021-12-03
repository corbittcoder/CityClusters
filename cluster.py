import sys
import googlemaps
import knn

import pandas as pd

if __name__ == '__main__':
    api = ""
    area = ""
    if len(sys.argv) != 4:
        print('Usage: cluster.py <GOOGLE DISTANCE MATRIX API KEY> <CITY NAME> <NUM GROUPS>')
        exit(1)
    else:
        api = sys.argv[1]
        area = sys.argv[2]
        try:
            NUM_GROUPS = int(sys.argv[3])
        except:
            print('Usage: cluster.py <GOOGLE DISTANCE MATRIX API KEY> <CITY NAME> <NUM GROUPS>')

    df = pd.read_csv(r"files\\" + area + ".csv") #New_York_City.csv
    # df = df.sort_values("City")
    # df = df.drop_duplicates(subset='City', keep='first')
    gmaps = googlemaps.Client(key=api)
    places = []#['Orange,Orange,TX', 30.0929879, -93.7365549, 'Red'],['Kountze,Hardin,TX', 30.3715975, -94.31241159999999, 'Blue']
    # colors = ['Red', 'Blue', 'Purple', 'Green'] #colors of groups
    errors = []
    for index, row in df.iterrows():
        address = row['Address'] + ", " + row['City'] + "," + row['State'] + "," + str(row['Zip code full'])
        try:
            coordinates = gmaps.geocode(address)[0]['geometry']['location']
            places.append([address, coordinates['lat'], coordinates['lng'], index % NUM_GROUPS,
                           row['Visitation frequency'], row['Total hours'], row['Zip Code']]) #assign colors randomly at start
            print(index)
        except:
            print("Place not found: " + address)
            errors.append(address)
    placesdf = pd.DataFrame(places, columns=['Address', 'Lat', 'Lng', 'Color', 'NumVisits', 'Hours', 'ShortZip'])
    try:
        placesdf.to_csv('files\\' + area + '_values.csv', index = False)
    except:
        print("Couldn't save")
    pd.DataFrame(errors).to_csv('files\\' + area + '_errors.csv', index = False)
    knn.main(placesdf, area, NUM_GROUPS, api)
