import pandas as pd
import os
import csv
import math
import time

def calc_distance(coords1, coords2):
    """
    Calculate distance between two lat,long point
    """
    return math.sqrt((coords1[0] - coords2[0])**2 + (coords1[1] - coords2[1])**2)

# script to join wheater station ids to counting points description dataset

zeitanfang = time.time()

from_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), "datasets", "counting_points", "Jawe2019.csv");
to_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), "datasets", "counting_points", "counting_point_wheater.csv");
wheater_station_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), "wheater_stations", "description_tu_rr.csv");

write_file = open(to_path, 'w', newline='');
writer = csv.writer(write_file);

with open(from_path) as csvfile:
    datareader = csv.reader(csvfile, delimiter=";");
    header = next(datareader);
    # new column for station id
    header[len(header) - 1] = "STATIONID";
    writer.writerow(header);

    for row in datareader:
        with open(wheater_station_path) as ws:

            wsReader = csv.reader(ws);            
            next(wsReader);
            # set distance to high value
            minimalDistance = 9999999999;
            minimalDistanceId = -1;

            if(row[195] != "" and row[196] != ""):
                for wsRow in wsReader:
                    # column 195 lat, column 196 long; column 4 lat, column 5 long
                    calculatedDistance = calc_distance([float(row[195].replace(",",".")), float(row[196].replace(",","."))], [float(wsRow[4]), float(wsRow[5])]);
                    if(calculatedDistance < minimalDistance):
                        minimalDistance = calculatedDistance;
                        minimalDistanceId = wsRow[0];
        
        row[len(row) - 1] = minimalDistanceId;
        writer.writerow(row);

zeitende = time.time()
print("Dauer Programmausführung: ");
print(zeitende-zeitanfang);