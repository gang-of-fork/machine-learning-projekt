#Script to merge weatherdata from the year 2019
#output from this script can be downloaded here https://drive.google.com/file/d/1KmNOf1ygsXnV1vWRtdKUJrR8b0CMMp8C/view?usp=sharing

import os
import pandas as pd
import json

#read relevant stations
fobj = open("relevant_station_ids.json")

relevant_stations = json.load(fobj)

fobj.close()

FILE_BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "datasets", "wetter_entpackt")

NIEDERSCHLAG_PATH = os.path.join(FILE_BASE_PATH, "niederschlag")
TEMPERATUR_PATH = os.path.join(FILE_BASE_PATH, "temperatur")

niederschlag_dirs = os.listdir(NIEDERSCHLAG_PATH)
temperatur_dirs = os.listdir(TEMPERATUR_PATH)

def get_filename_filter(id):
    return lambda fname: id in fname[:24]

ctr = 1

joined_nieder_dfs = []
joined_temp_dfs = []

for id in relevant_stations:
    print(str(ctr) + " of " + str(len(relevant_stations)))

    filename_filter = get_filename_filter(id)

    nieder_dir = list(filter(filename_filter, niederschlag_dirs))
    temp_dir = list(filter(filename_filter, temperatur_dirs))

    if not(len(nieder_dir) == 1 and len(temp_dir) == 1):
        continue
    
    nieder_dir_path = os.path.join(NIEDERSCHLAG_PATH, nieder_dir[0])
    temp_dir_path = os.path.join(TEMPERATUR_PATH, temp_dir[0])

    nieder_file = list(filter(get_filename_filter("produkt_rr_stunde_"), os.listdir(nieder_dir_path)))[0]
    temp_file = list(filter(get_filename_filter("produkt_tu_stunde_"), os.listdir(temp_dir_path)))[0]

    nieder_data_df = pd.read_csv(os.path.join(nieder_dir_path, nieder_file), sep=";")
    temp_data_df = pd.read_csv(os.path.join(temp_dir_path, temp_file), sep=";")

    #filter data of 2019
    joined_nieder_dfs.append(nieder_data_df[(nieder_data_df["MESS_DATUM"] >= 2019010100) & (nieder_data_df["MESS_DATUM"] <= 2019123123)])
    joined_temp_dfs.append(temp_data_df[(temp_data_df["MESS_DATUM"] >= 2019010100) & (temp_data_df["MESS_DATUM"] <= 2019123123)])

    ctr += 1

joined_nieder_all_df = pd.concat(joined_nieder_dfs)

joined_nieder_all_df.merge(pd.concat(joined_temp_dfs), on=["STATIONS_ID", "MESS_DATUM"]).to_csv("weatherdata_2019_v2.csv")
