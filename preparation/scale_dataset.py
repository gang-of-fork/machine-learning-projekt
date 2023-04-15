from pandas import read_csv
from sklearn.preprocessing import StandardScaler
from joblib import dump

dataset = read_csv('../datasets/accidents_small_unscaled.csv',
                   delimiter=',', index_col=True)

print(dataset.describe())

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
print(temperature_scaler.mean_)

percipitation_scaler = StandardScaler().fit(
    dataset["percipitation"].to_numpy().reshape(-1, 1))
print(percipitation_scaler.mean_)

# scale the remaining rows


def scaleRow(row):
    row["accidents"] = scaler_per_weatherstation_dict[row["weather_station"]
                                                      ].transform([[row["accidents"]]])
    row["temperature"] = temperature_scaler.transform([[row["temperature"]]])
    row["percipitation"] = percipitation_scaler.transform(
        [[row["percipitation"]]])
    return row


dataset = dataset.apply(scaleRow, axis=1)

# drop rows not needed for prediction
dataset = dataset.drop(['weather_station'])

dataset.to_csv('../datasets/accidents_small.csv', index=None)
