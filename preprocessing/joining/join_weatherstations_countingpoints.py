#Script to join weatherdata and countingpoints

import os
import sys
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler

weatherdata_path = os.path.join(os.path.dirname(
    __file__), "weatherdata_2019_v8_A.csv")

weatherdata_df = pd.read_csv(weatherdata_path)

select_complete_weather_stations_path = os.path.join(os.path.dirname(__file__), ".." "", "output", "ws_complete_zaehlstellen.json")

fobj = open(select_complete_weather_stations_path, "r")

weatherstation_counting_station_mapping = json.load(fobj)

fobj.close()

print("finished reading zaehlstellen")

#A_S_path = os.path.join(os.path.dirname(__file__), "datasets", "zaehlstellen_entpackt", "2019_A_S", "2019_A_S.txt")
B_S = os.path.join(os.path.dirname(__file__), ".." "datasets", "counting_points", "2019_B_S", "2019_B_S.txt")

#A_S_data_df = pd.read_csv(A_S_path, sep=";")
B_data_df = pd.read_csv(B_S, sep=";")

print("finished reading A DF")


auslastung_values = []

ctr = 0
to_process = len(weatherdata_df.index)

standard_scaler_map = {}

for weatherdata_index, weatherdata_row in weatherdata_df.iterrows():
    try:
        tk_numbers = weatherstation_counting_station_mapping[str(
            weatherdata_row["STATIONS_ID"])]
    except:
        auslastung_values.append("")
        continue

    d = int(str(weatherdata_row["MESS_DATUM"])[2:8])
    hour = int(str(weatherdata_row["MESS_DATUM"])[8:])

    if hour == 0:
        hour = 24

    ausl_data = []

    #create standardcaler for every counting points
    for ausl_station_id in tk_numbers: #tk_numbers contains counting stations for current weatherstations
        if not int(ausl_station_id) in standard_scaler_map.keys():
            counting_station_r1_values = B_data_df[B_data_df["Zst"]
                                                     == ausl_station_id]["KFZ_R1"].tolist() #KFZ_R1 and KFZ_R2 are values for both street directions

            if len(counting_station_r1_values) == 0: #is 0 if is of opposite type
                continue

            counting_station_r1_values_NP = np.array(
                [int(v) for v in counting_station_r1_values]).reshape(-1, 1)

            counting_station_r2_values = B_data_df[B_data_df["Zst"]
                                                     == ausl_station_id]["KFZ_R2"].tolist()
            counting_station_r2_values_NP = np.array(
                [int(v) for v in counting_station_r2_values]).reshape(-1, 1)

            scalerR1 = StandardScaler()
            scalerR1.fit(counting_station_r1_values_NP)

            scalerR2 = StandardScaler()
            scalerR2.fit(counting_station_r2_values_NP)

            standard_scaler_map[int(ausl_station_id)] = {
                "r1": scalerR1,
                "r2": scalerR2
            }

    #for ausldata_index, ausldata_row in A_S_data_df[(A_S_data_df["Zst"].isin(tk_numbers)) & (A_S_data_df["Datum"] == d) & (A_S_data_df["Stunde"] == hour)].iterrows():
    for ausldata_index, ausldata_row in B_data_df[(B_data_df["Zst"].isin(tk_numbers)) & (B_data_df["Datum"] == d) & (B_data_df["Stunde"] == hour)].iterrows():
        # B_data_df[(B_data_df["Zst"].isin(tk_numbers))]

        #use standardscaler
        scaled_r1 = standard_scaler_map[int(ausldata_row["Zst"])]["r1"].transform([[
            ausldata_row["KFZ_R1"]]])
        scaled_r2 = standard_scaler_map[int(ausldata_row["Zst"])]["r2"].transform([[
            ausldata_row["KFZ_R2"]]])

        ausl_data.append(
            str(ausldata_row["Zst"]) + ":" +
            str(scaled_r1[0][0]) + ":" + str(scaled_r2[0][0])
        )

    auslastung_values.append("|".join(ausl_data))

    ctr += 1

    if ctr % 500 == 0:
        print(str(ctr) + " of " + str(to_process))

print(len(auslastung_values))

weatherdata_df["AuslastungB"] = auslastung_values
#weatherdata_df["AuslastungA"] = auslastung_values

#weatherdata_df.to_csv("weatherdata_2019_v8_A.csv")
weatherdata_df.to_csv("weatherdata_2019_v8_AB.csv")
print("finished")
