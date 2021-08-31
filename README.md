# CityClusters
Given a list of cities, groups them by area. 

Running cluster.py <GOOGLE DISTANCE MATRIX API KEY> <CITY NAME> <NUM GROUPS> will take a CSV file named city_name.csv and run a list of addresses through Google Maps to get the coordinates. 
(Note: the file must have a column named "City" and a column named "State" to work, those are the values it uses.)
Then it will print out a CSV file (files/[city_name]_values.csv) with the coordinates of each location.
It then automatically runs the next step, knn.py.

You can also rerun knn.py manually (for instance, if some locations in the [city_name]_values.csv file need to be manually changed before grouping).
On running knn.py <GOOGLE API KEY> <CITY NAME> <NUM GROUPS>, knn.py takes the file output at the last step and runs a KNN clustering algorithm on them.
It output a CSV file (files/[city_name]_results.csv) with each data point and the number of its assigned group. 
It then automatically runs the final step, plot.py.

You can also run plot.py manually (for instance, if you want the group assigned a  the KNN classifier in the file from the last step). 
On running plot.py <GOOGLE API KEY> <CITY NAME> <NUM GROUPS>, plot.py takes the output from the last step and plots it onto a map.
Each data point will appear in its location with a pin colored by group. 
The current maximum number of colors is 10, so care should be taken about classifying into more groups than this.

All steps automatically run in sequence. 
