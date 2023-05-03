from pandas import read_csv
import numpy as np
from sklearn.preprocessing import StandardScaler
from joblib import dump
from datetime import datetime

starttime = datetime.now()
RESCALE_ACCIDENTS = True

print("loading dataset...")

dataset = read_csv('../datasets/accidents_raw.csv',
                   delimiter=',')


# group by 2 hour cycles


def transform_hours_2h(row):
    hour = row["hour"]
    if 0 <= hour <= 1:
        row["hour"] = 0
    if 2 <= hour <= 3:
        row["hour"] = 1
    if 4 <= hour <= 5:
        row["hour"] = 2
    if 6 <= hour <= 7:
        row["hour"] = 3
    if 8 <= hour <= 9:
        row["hour"] = 4
    if 10 <= hour <= 11:
        row["hour"] = 5
    if 12 <= hour <= 13:
        row["hour"] = 6
    if 14 <= hour <= 15:
        row["hour"] = 7
    if 16 <= hour <= 17:
        row["hour"] = 8
    if 18 <= hour <= 19:
        row["hour"] = 9
    if 20 <= hour <= 21:
        row["hour"] = 10
    if 22 <= hour <= 23:
        row["hour"] = 11
    return row


print("transforming and grouping by hours... (this may take a few minutes)")

dataset = dataset.apply(transform_hours_2h, axis=1)
dataset = dataset.groupby(['weather_station', 'month', 'day', 'hour']).agg(
    {'temperature': 'mean', 'percipitation': 'mean', 'road_usage': 'mean', 'accidents': 'sum'}).reset_index()


# extract distinct weather_station ids
weatherstation_ids = dataset["weather_station"].drop_duplicates().to_numpy(
    dtype='int')

print(f'Dataset has {len(weatherstation_ids)} distinct weather stations')

scaler_per_weatherstation_dict = {}

# only use the neccessary columns for the fitting of the scalers to minimize computing time
dataset_reduced_columns = dataset[["weather_station", "accidents"]]

print("fitting scalers...")
# fit the accidents-scalers for every weatherstation
for weatherstation_id in weatherstation_ids:
    # filter accident counts for this weatherstation and transform to numpy array to prepare for sklearn scaler fitting
    accident_counts = dataset_reduced_columns[
        dataset_reduced_columns["weather_station"] == weatherstation_id].drop("weather_station", axis=1).to_numpy(dtype='int')

    scaler = StandardScaler().fit(accident_counts)

    # add the scaler to the mapping and save in the scalers directory for later use
    scaler_per_weatherstation_dict[weatherstation_id] = scaler
    dump(scaler, f'../scalers/accident_scaler_{weatherstation_id}.bin')

# fit scalers for the remaining unscaled features
temperature_scaler = StandardScaler().fit(
    dataset["temperature"].to_numpy().reshape(-1, 1))
percipitation_scaler = StandardScaler().fit(
    dataset["percipitation"].to_numpy().reshape(-1, 1))

# transform the remaining features


def transformRow(row):
    if RESCALE_ACCIDENTS:
        row["accidents_scaled"] = scaler_per_weatherstation_dict[row["weather_station"]
                                                                 ].transform([[row["accidents"]]])[0][0]
    row["temperature"] = temperature_scaler.transform([[row["temperature"]]])
    row["percipitation"] = percipitation_scaler.transform(
        [[row["percipitation"]]])
    return row


print("transforming rows... (this may take a few minutes)")
dataset = dataset.apply(transformRow, axis=1)

dataset.to_csv('../datasets/accidents.csv', index=None)

print(dataset.describe())

print("Correlation Matrix:")
print(dataset.corr())

print("\nDistribution of accidents:")
print(dataset['accidents'].value_counts())


print(f'Execution Time: {datetime.now() - starttime }')
