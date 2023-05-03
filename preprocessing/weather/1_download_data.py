#Script to download weatherdata from dwd website
#!!!!! Before executing this script please follow instructions from preprocessing/datasets/wetter/README.txt !!!!!

import json
import os
import requests 


def downloadWeatherdata(url, filename, output): #function to download data and write zip file
    fobj = open(os.path.join(os.path.dirname(__file__), "..",  "output", "convert_and_filter_description", filename))

    data = json.loads("".join(fobj.readlines()))

    ctr = 0

    for i, zip_file in enumerate(data):
        print("writing " + str(i) + " : " + zip_file)

        request_url = url + zip_file
        r = requests.get(request_url)

        if r.status_code == 404:
            ctr += 1
            continue

        output_file = open(os.path.join(os.path.dirname(__file__), "..", "datasets", "wetter", output, zip_file), "wb")

        output_file.write(r.content)

        output_file.close()

        print("finished " + str(i) + " of " + str(len(data)))

    fobj.close()

    print(str(ctr))

    print("---- finished ----")

if __name__ == "__main__":
    #download niederschlag
    downloadWeatherdata("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/precipitation/historical/", "relevant_data_RR.json", "niederschlag")

    #download temperatur
    downloadWeatherdata("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/", "relevant_data_TU.json", "temperatur")