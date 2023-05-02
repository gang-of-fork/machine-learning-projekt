from pandas import read_csv
import pandas as pd
from sklearn.model_selection import train_test_split
from datetime import datetime
import matplotlib.pyplot as plt

starttime = datetime.now()
RESCALE_ACCIDENTS = True

print('loading dataset...')

dataset = read_csv('../datasets/accidents.csv')

print(dataset.describe())

print("Correlation Matrix:")
print(dataset.corr())

print("\nDistribution of accidents:")
print(dataset['accidents'].value_counts())

# Split into variables and target
X = dataset.drop('accidents_scaled', axis=1)
y = dataset['accidents_scaled']

# Split into train and test dataset and save to csv
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2)

X_test['weather_station'].to_csv(
    '../datasets/accidents_weatherstations.csv', index=None)

print('dropping weather_station...')
X_train = X_train.drop('weather_station', axis=1)
X_test = X_test.drop('weather_station', axis=1)

y_train = pd.DataFrame(y_train)

print('distribution of accidents in X_train:')
print(X_train['accidents'].value_counts())
print('equalizing distribution of accidents in the training sets')

# only keep every 18th of the 0 accident datapoints
rows_to_delete = X_train[(X_train['accidents'] == 0) & (
    X_train.reset_index().index % 10 != 0)].index
X_train = X_train.drop(rows_to_delete)
y_train = y_train.drop(rows_to_delete)

# only keep every 7th of 1 accident datapoints
rows_to_delete = X_train[(X_train['accidents'] == 1) & (
    X_train.reset_index().index % 5 != 0)].index
X_train = X_train.drop(rows_to_delete)
y_train = y_train.drop(rows_to_delete)

# only keep every 3rd of 2 accident datapoints
rows_to_delete = X_train[(X_train['accidents'] == 2) & (
    X_train.reset_index().index % 2 != 0)].index
X_train = X_train.drop(rows_to_delete)
y_train = y_train.drop(rows_to_delete)

# only keep 50% of 3 accident datapoints
rows_to_delete = X_train[(X_train['accidents'] == 3) & (
    X_train.reset_index().index % 1 != 0)].index
X_train = X_train.drop(rows_to_delete)
y_train = y_train.drop(rows_to_delete)

print('distribution of accidents in X_train:')
print(X_train['accidents'].value_counts())
X_train['accidents'].value_counts().plot.bar()
plt.show()

print('dropping accidents from the datasets...')

X_train = X_train.drop('accidents', axis=1)
X_test = X_test.drop('accidents', axis=1)

# X_train.to_csv("../datasets/accidents_X_train.csv", index=None)
# X_test.to_csv("../datasets/accidents_X_test.csv", index=None)
# y_train.to_csv("../datasets/accidents_y_train.csv", index=None)
# y_test.to_csv("../datasets/accidents_y_test.csv", index=None)


print(f'Execution Time: {datetime.now() - starttime }')
