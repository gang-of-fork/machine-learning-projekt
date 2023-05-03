#Script to select only those weather stations that only have counting points with complete datasets
#this is nessecary to ensure that data can be scaled properly and no missing counting point data influences results

import os
import sys
import pandas as pd
import json

weatherdata_path = os.path.join(os.path.dirname(__file__), "weatherdata_2019_v2.csv") #can be downloaded here https://drive.google.com/file/d/1KmNOf1ygsXnV1vWRtdKUJrR8b0CMMp8C/view?usp=sharing

weatherdata_df = pd.read_csv(weatherdata_path)

weather_counting_point_path = os.path.join(os.path.dirname(__file__), "..", "datasets", "counting_points", "counting_point_weather.csv")

weather_counting_point_df = pd.read_csv(weather_counting_point_path, on_bad_lines='skip')

ctr = 0

weatherstation_counting_station_mapping = {}

for stationid in weatherdata_df.STATIONS_ID.unique():
    counting_stations = weather_counting_point_df[(weather_counting_point_df["STATIONID"] == stationid)]
    if len(counting_stations.index) == 0:
        continue
    
    weatherstation_counting_station_mapping[str(stationid)] = list(counting_stations.DZ_Nr.unique())


fobj = open("zaehlstellen_entry_count.json", "r")

zaehlstationen_completeness_data = json.load(fobj)

fobj.close()    



weatherstation_countingstation_mapping_completeness = {}

for ws in weatherstation_counting_station_mapping.keys():
    weatherstation_countingstation_mapping_completeness[ws] = []
    for zs in weatherstation_counting_station_mapping[ws]:
        if zaehlstationen_completeness_data[str(zs)] == 8760:
            weatherstation_countingstation_mapping_completeness[ws].append(True)
        else:
            weatherstation_countingstation_mapping_completeness[ws].append(False)

complete_weather_stations = [k for k in weatherstation_countingstation_mapping_completeness.keys() if all(weatherstation_countingstation_mapping_completeness[k]) ]

final_mapping = {}

for ws in weatherstation_counting_station_mapping:
    if ws in complete_weather_stations:
        final_mapping[int(ws)] = [ int(w) for w in weatherstation_counting_station_mapping[ws] ]

#output a file of all weather stations that only have counting stations with complete data
output_path = os.path.join(os.path.dirname(__file__), "..", "output", "select_complete_weather_stations", 'ws_complete_zaehlstellen.json')

with open(output_path, 'w', encoding='utf-8') as f:
  f.write(json.dumps(final_mapping, ensure_ascii=False))
    