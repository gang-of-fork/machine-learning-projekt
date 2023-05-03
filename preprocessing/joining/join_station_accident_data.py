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

# script to join wheater stations ids to accident dataset

start = time.time()

from_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), "datasets", "accidents", "unfalldaten_2019.csv");
to_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), "datasets", "accidents", "accident_station_data.csv");
wheater_station_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), "wheater_stations", "description_tu_rr.csv");

write_file = open(to_path, 'w', newline='');
writer = csv.writer(write_file);

with open(from_path) as csvfile:
    datareader = csv.reader(csvfile);
    header = next(datareader);
    # new column for station id
    header.append("STATIONID")
    writer.writerow(header);

    for row in datareader:
        with open(wheater_station_path) as wheater:
            
            wheaterReader = csv.reader(wheater);            
            next(wheaterReader);
            # reset minimal distance to high value
            minimalDistance = 999999;
            minimalDistanceId = -1;

            for wheaterRow in wheaterReader:
                calculatedDistance = calc_distance([float(row[25]), float(row[24])], [float(wheaterRow[4]), float(wheaterRow[5])]);
                if(calculatedDistance < minimalDistance):
                    minimalDistance = calculatedDistance;
                    minimalDistanceId = wheaterRow[0];
        
        row.append(minimalDistanceId);
        writer.writerow(row);

end = time.time()
print("Dauer Programmausführung:",);
print(end-start);

# bring joind dataset to csv file
read_file = pd.read_csv(to_path);
