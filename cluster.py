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
    # places = knn(placesdf)
    # places.to_csv('files\\houston_results.csv', index=False)
    #
    # gmap = gmplot.GoogleMapPlotter.from_geocode("Houston, Texas", apikey=api)
    # for i in range(len(colors)):
    #     group = places[places.Color == i]
    #     gmap.scatter(group.Lat.tolist(), group.Lng.tolist(), color=colors[i])
    # gmap.draw("C:\\Users\\scttc\\PycharmProjects\\CityClusters\\houston_map.html")
    # distances = pd.DataFrame(columns = places, index = places)
    # print(distances)
    # for i, row in distances.iterrows():
    #     for j, column in row.iteritems():
    #
    #         #check if work already done, if so then copy over value. If not then get distance.
    #         if not type(distances[j][i]) == float:
    #             distances[i][j] = distances[j][i]
    #         elif i == j:
    #             distances[i][j] = 0
    #         else:
    #             distances[i][j] = payload(i, j, api)
    #     print(distances)
    # plot(distances, api)



# def payload(origin, destination, api):
#     query = "https://maps.googleapis.com/maps/api/distancematrix/json?"
#     payload = {
#         'origins' : origin,
#         'destinations' : destination,
#         'mode' : 'driving',
#         'key' : api
#     }
#
#     r = requests.get(query, params = payload)
#
#     if r.status_code != 200:
#         print('HTTP status code {} received, program terminated.'.format(r.status_code))
#     else:
#         try:
#             x = json.loads(r.text)
#             print(x)
#
#             # Now you can do as you please with the data structure stored in x.
#             # Here, we print it as a Cartesian product.
#             for isrc, src in enumerate(x['origin_addresses']):
#                 for idst, dst in enumerate(x['destination_addresses']):
#                     row = x['rows'][isrc]
#                     cell = row['elements'][idst]
#                     if cell['status'] == 'OK':
#                         print (x)
#                         return cell['distance']['text'].split( )[0]
#                     else:
#                         print('{} to {}: status = {}'.format(src, dst, cell['status']))
#
#             # Of course, we could have also saved the results in a file,
#             with open('gdmpydemo.json', 'w') as f:
#                 f.write(r.text)
#
#         # TODO Or in a database
#
#         except ValueError:
#             print('Error while parsing JSON response, program terminated.')
