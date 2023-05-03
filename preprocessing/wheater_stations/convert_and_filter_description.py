# script to convert wheater station description text file to filtered csv file
# json output with all file names of wheater stations working in 2019

import pandas as pd
import os
import csv
import json

listed_dir = os.listdir(os.path.dirname(__file__));
print(listed_dir);

for i, file in enumerate(listed_dir):
    # check for all description files
    if(file.endswith(".txt") and file.startswith("description")):
        file_name = file.split(".")[0]
        data_type = file_name.split("_")[1]
        file_type = file_name.split("_")[2]

        txt_path = os.path.join(os.path.dirname(__file__), f"{file_name}.txt");
        csv_path = os.path.join(os.path.dirname(__file__), f"{file_name}.csv");
        json_path = os.path.join(os.path.dirname(__file__), "..", "output", "convert_and_filter_description", f"relevant_data_{file_type}.json");

        read_file = pd.read_csv(txt_path, delim_whitespace=True, skiprows=[1], usecols=range(0, 6));

        # filter for wheater stations working in 2019
        filtered_file = read_file[read_file['von_datum'] < 20190101][read_file['bis_datum'] > 20191231];

        # convert filtered txt to csv to use all data
        filtered_file.to_csv(csv_path,  index=False);

        # wrtie list with file names of weather stations
        list = [];
        with open(csv_path) as csvfile:
            datareader = csv.reader(csvfile)
            next(datareader); 
            for row in datareader:
                # needed to limit date because of errors after dataset update
                list.append(f"{data_type}_{file_type}_{(5-len(str(row[0])))*'0'}{row[0]}_{row[1]}_{row[2] if int(row[2]) < 20221231 else 20221231}_hist.zip")

        # json output for relevant_data_*.json
        with open(json_path, "w") as outfile:
            json.dump(list, outfile);
