import os
import json
import csv

# script to eliminate differences between description for RR and TU 
# data from 

csv_path_rr = os.path.join(os.path.dirname(__file__), "description_stundenwerte_RR.csv");
csv_path_tu = os.path.join(os.path.dirname(__file__), "description_stundenwerte_TU.csv");

with open(csv_path_rr, 'r') as t1, open(csv_path_tu, 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

list_rr_ids = [];
for line in fileone:
    list_rr_ids.append(line.split(",")[0]);

list_tu_ids = [];
for line in filetwo:
    list_tu_ids.append(line.split(",")[0]);
    
diff = list(set(list_tu_ids) - (set(list_tu_ids) - set(list_rr_ids)));

csv_path_tu_rr = os.path.join(os.path.dirname(__file__), "description_tu_rr.csv");

with open(csv_path_tu, "r") as readfile:
    datareader = csv.reader(readfile);
    with open(csv_path_tu_rr, "w", newline="") as writefile:
        datawriter = csv.writer(writefile);    
        header = next(datareader);
        datawriter.writerow(header);
        for row in datareader:
            if(row[0] in diff):
                datawriter.writerow(row);

for index, value in enumerate(diff):
    diff[index] =  (5-len(str(value)))*'0' + value;





