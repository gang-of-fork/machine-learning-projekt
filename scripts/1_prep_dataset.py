from pandas import read_csv
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from joblib import dump
from sklearn.model_selection import train_test_split
from random import randint


dataset = read_csv('../datasets/accidents_small_unscaled_90.csv',
                   delimiter=',')

# group by 4 hour cycles


def transform_hours_4h(row):
    hour = row["hour"]
    if 0 <= hour <= 3:
        row["hour"] = 0
    if 4 <= hour <= 7:
        row["hour"] = 1
    if 8 <= hour <= 11:
        row["hour"] = 2
    if 12 <= hour <= 15:
        row["hour"] = 3
    if 16 <= hour <= 19:
        row["hour"] = 4
    if 20 <= hour <= 23:
        row["hour"] = 5
    return row


def transform_hours_6h(row):
    hour = row["hour"]
    if 4 <= hour <= 9:
        row["hour"] = 0
    if 10 <= hour <= 15:
        row["hour"] = 1
    if 16 <= hour <= 21:
        row["hour"] = 2
    if 22 <= hour <= 23 & 0 <= hour <= 3:
        row["hour"] = 3
    return row


dataset = dataset.apply(transform_hours_4h, axis=1)
dataset = dataset.groupby(['weather_station', 'month', 'day', 'hour']).agg(
    {'temperature': 'mean', 'percipitation': 'mean', 'road_usage': 'mean', 'accidents': 'sum'}).reset_index()

# print('distribution of accidents')
# print(dataset['accidents'].value_counts(), '\n')

# columns_to_delete = dataset[(dataset['accidents'] == 0) & (
#    dataset.reset_index().index % 8 != 0)].index
# dataset = dataset.drop(columns_to_delete)

# columns_to_delete = dataset[(dataset['accidents'] == 1) & (
#    dataset.reset_index().index % 2 != 0)].index
# dataset = dataset.drop(columns_to_delete)

# print('distribution of accidents after equalizing')
# print(dataset['accidents'].value_counts())


# extract distinct weather_station ids
weatherstation_ids = dataset["weather_station"].drop_duplicates().to_numpy(
    dtype='int')

scaler_per_weatherstation_dict = {}

# only use the neccessary columns for the fitting of the scalers to minimize computing time
dataset_reduced_columns = dataset[["weather_station", "accidents"]]

# fit the accidents-scalers for every weatherstation
for weatherstation_id in weatherstation_ids:
    # filter accident counts for this weatherstation and transform to numpy array to prepare for sklearn scaler fitting
    accident_counts = dataset_reduced_columns[
        dataset_reduced_columns["weather_station"] == weatherstation_id].drop("weather_station", axis=1).to_numpy(dtype='int')

    scaler = StandardScaler().fit(accident_counts)

    # add the scaler to the mapping and save in the scalers directory for later use
    scaler_per_weatherstation_dict[weatherstation_id] = scaler
    dump(scaler, f'../scalers/accident_scaler_{weatherstation_id}.bin')

# fit scalers for the remaining unscaled rows
temperature_scaler = StandardScaler().fit(
    dataset["temperature"].to_numpy().reshape(-1, 1))
percipitation_scaler = StandardScaler().fit(
    dataset["percipitation"].to_numpy().reshape(-1, 1))

# transform the remaining rows


def transformRow(row):
    # scale features
    # row["accidents"] = scaler_per_weatherstation_dict[row["weather_station"]
    #                                                  ].transform([[row["accidents"]]])

    row["temperature"] = temperature_scaler.transform([[row["temperature"]]])
    row["percipitation"] = percipitation_scaler.transform(
        [[row["percipitation"]]])
    return row


dataset = dataset.apply(transformRow, axis=1)

# transform cyclic features
dataset['sin_hour'] = np.sin(2*np.pi*dataset['hour']/6)
dataset['cos_hour'] = np.cos(2*np.pi*dataset['hour']/6)
dataset = dataset.drop('hour', axis=1)

dataset['sin_day'] = np.sin(2*np.pi*(dataset['day']-1)/7)
dataset['cos_day'] = np.cos(2*np.pi*(dataset['day']-1)/7)
dataset = dataset.drop('day', axis=1)


# Split into variables and target
X = dataset.drop('accidents', axis=1)
y = dataset['accidents']

# Split into train and test dataset and save to csv
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2)

X_test['weather_station'].to_csv(
    '../datasets/accidents_small_weatherstations.csv', index=None)

# drop rows not needed for prediction
X_train = X_train.drop(
    ['weather_station', 'month', 'sin_day', 'cos_day'], axis=1)
X_test = X_test.drop(['weather_station', 'month',
                     'sin_day', 'cos_day'], axis=1)

y_train = pd.DataFrame(y_train)


print(y_train['accidents'].value_counts())
print('equalizing distribution of accidents in the training sets')

columns_to_delete = y_train[(y_train['accidents'] == 0) & (
    y_train.reset_index().index % 6 != 0)].index
X_train = X_train.drop(columns_to_delete)
y_train = y_train.drop(columns_to_delete)

columns_to_delete = y_train[(y_train['accidents'] == 1) & (
    y_train.reset_index().index % 2 != 0)].index
X_train = X_train.drop(columns_to_delete)
y_train = y_train.drop(columns_to_delete)

print(y_train['accidents'].value_counts())

X_train.to_csv("../datasets/accidents_small_X_train.csv", index=None)
X_test.to_csv("../datasets/accidents_small_X_test.csv", index=None)
y_train.to_csv("../datasets/accidents_small_y_train.csv", index=None)
y_test.to_csv("../datasets/accidents_small_y_test.csv", index=None)

dataset.to_csv('../datasets/accidents_small.csv', index=None)
print(dataset.describe())
print(dataset.corr())