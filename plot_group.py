import pandas as pd
import gmplot
import seaborn as sns
import sys

def plot(places, name, groupNum, api):
    #plot data points on map
    colors = ["#000000", "#000080", "#00008B", "#0000CD", "#0000FF", "#006400", "#008000", "#008080", "#008B8B", "#00BFFF", "#00CED1", "#00FA9A", "#00FF00", "#00FF7F", "#00FFFF", "#191970", "#1E90FF", "#20B2AA", "#228B22", "#2E8B57", "#2F4F4F", "#32CD32", "#3CB371", "#40E0D0", "#4169E1", "#4682B4", "#483D8B", "#48D1CC", "#4B0082", "#556B2F", "#5F9EA0", "#6495ED", "#66CDAA", "#696969", "#6A5ACD", "#6B8E23", "#708090", "#778899", "#7B68EE", "#7CFC00", "#7FFF00", "#7FFFD4", "#800000", "#800080", "#808000", "#808080", "#87CEEB", "#87CEFA", "#8A2BE2", "#8B0000", "#8B008B", "#8B4513", "#8FBC8F", "#90EE90", "#9370DB", "#9400D3", "#98FB98", "#9932CC", "#9ACD32", "#A0522D", "#A52A2A", "#A9A9A9", "#ADD8E6", "#ADFF2F", "#AFEEEE", "#B0C4DE", "#B0E0E6", "#B22222", "#B8860B", "#BA55D3", "#BC8F8F", "#BDB76B", "#C0C0C0", "#C71585", "#CD5C5C", "#CD853F", "#D2691E", "#D2B48C", "#D3D3D3", "#D8BFD8", "#DA70D6", "#DAA520", "#DB7093", "#DC143C", "#DCDCDC", "#DDA0DD", "#DEB887", "#E0FFFF", "#E6E6FA", "#E9967A", "#EE82EE", "#EEE8AA", "#F08080", "#F0E68C", "#F0F8FF", "#F0FFF0", "#F0FFFF", "#F4A460", "#F5DEB3", "#F5F5DC", "#F5F5F5", "#F5FFFA", "#F8F8FF", "#FA8072", "#FAEBD7", "#FAF0E6", "#FAFAD2", "#FDF5E6", "#FF0000", "#FF00FF", "#FF1493", "#FF4500", "#FF6347", "#FF69B4", "#FF7F50", "#FF8C00", "#FFA07A", "#FFA500", "#FFB6C1", "#FFC0CB", "#FFD700", "#FFDAB9", "#FFDEAD", "#FFE4B5", "#FFE4C4", "#FFE4E1", "#FFEBCD", "#FFEFD5", "#FFF0F5", "#FFF5EE", "#FFF8DC", "#FFFACD", "#FFFAF0", "#FFFAFA", "#FFFF00", "#FFFFE0", "#FFFFF0", "#FFFFFF"]
    # colors = sns.color_palette(colorOptions, numGroups, as_cmap=True)
    # colors = list(map(lambda x: '#%02x%02x%02x' % (int(x[0]*255), int(x[1]*255), int(x[2]*255)), palette))
    # colors = ['magenta', 'turquoise', 'red', 'blue', 'green', 'yellow', 'purple', 'pink', 'orange', 'brown'] #colors of groups
    colors = sns.color_palette(colors, numGroups, as_cmap=True)
    gmap = gmplot.GoogleMapPlotter.from_geocode(name, apikey=api)
    group = places[places.Color == groupNum]
    gmap.scatter(group.Lat.tolist(), group.Lng.tolist(), color=colors[groupNum % len(colors)])
    gmap.draw(r"maps\\" + name + "_map.html")

if __name__ == '__main__':
    api = ''
    name = ''
    numGroups = 0
    try:
        api = sys.argv[1]
        name = sys.argv[2]
        groupNum = int(sys.argv[3])
    except:
        print('Usage: plot.py <GOOGLE API KEY> <CITY NAME> <GROUP NUM>')
    places = pd.read_csv(r"files\\" + name + "_results.csv")
    plot(places, name, groupNum, api)
