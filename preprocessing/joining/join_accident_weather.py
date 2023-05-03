#join accident and weather data based on weather station id

import pandas as pd
import math
import os
import datetime

accident_csv_path = os.path.join(os.path.dirname(__file__), "..", "datasets" , "accidents", "accident_station_data.csv")
accident_data_df = pd.read_csv(accident_csv_path)

weather_csv_path = os.path.join(os.path.dirname(__file__), "weatherdata_2019_v8_AB.csv")
weather_data_df = pd.read_csv(weather_csv_path)

"""
1 = Sonntag
2 = Montag
3 = Dienstag
4 = Mittwoch
5 = Donnerstag
6 = Freitag
7 = Samstag
"""

def get_possible_dates_in_month(month, weekday):
    start = datetime.datetime(2019, month, 1)
    end = datetime.datetime(start.year + int(start.month / 12), ((start.month % 12) + 1), 1)
    num_of_days = (end - start).days

    result = []

    for num_days_to_add in range(num_of_days):
        date_to_check = datetime.datetime(2019, month, 1 + num_days_to_add)
        if (((date_to_check.weekday() + 1) % 7) + 1) == weekday:
            result.append(date_to_check)
    
    return result

def avg(lst):
    if len(lst) == 0:
        #print("Err")
        return 0

    return round(sum(lst) / len(lst), 4)

def get_average_usage(ausl):
    val = 0

    get_avg_station_ausl = lambda aus: avg([float(aus.split(":")[1]), float(aus.split(":")[2])])

    if type(ausl) == str:
        return avg([ get_avg_station_ausl(a) for a in ausl.split("|") ])
    
    return None
    
def get_average_usage_values(ausl_values):
    notNone = lambda x: x != None

    return list(filter(notNone, [ get_average_usage(a) for a in ausl_values ]))
    

if __name__ == "__main__":
    result = []

    grouped_accidents = {}

    ctr = 0
    to_process = len(weather_data_df.STATIONS_ID.unique()) * 12 * 7 * 24

    for ws in weather_data_df.STATIONS_ID.unique():
        for month in range(1, 13): #iterate over months in year
            for day in range(1, 8): # iterate over weekdays in month
                possible_dates = [ d.strftime("%Y%m%d") for d in get_possible_dates_in_month(month, day) ] #calc possible dates

                for hour in range(24):
                    dates_formatted = [ int(d + (str(hour) if hour >= 10 else "0" + str(hour))) for d in possible_dates ]
                    weather_and_auslastung = weather_data_df[(weather_data_df["MESS_DATUM"].isin(dates_formatted)) & (weather_data_df["STATIONS_ID"] == ws)]
                    
                    num_of_accidents = len(accident_data_df[(accident_data_df["UMONAT"] == month) & (accident_data_df["UWOCHENTAG"] == day) & (accident_data_df["USTUNDE"] == hour) & (accident_data_df["STATIONID"] == ws)].index)

                    result.append({
                        "weather_station": ws,
                        "temperture": avg(weather_and_auslastung["TT_TU"].tolist()),
                        "percipitation": avg(weather_and_auslastung["  R1"].tolist()),
                        "month": month,
                        "day": day,
                        "hour": hour,
                        "accidents": num_of_accidents,
                        "road_usage": avg(get_average_usage_values(weather_and_auslastung["AuslastungA"].tolist()) + get_average_usage_values(weather_and_auslastung["AuslastungB"].tolist()))
                    })

                    ctr += 1

                    if ctr % 200 == 0:
                        print("Processed " + str(ctr) + " of " + str(to_process))

    df = pd.DataFrame.from_records(result)
    df.to_csv("data_v8.csv") #write dataframe