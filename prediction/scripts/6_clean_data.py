from pandas import read_csv

print("loading dataset...")

dataset = read_csv('../datasets/accidents_raw.csv',
                   delimiter=',')

print(len(dataset))
print('remove rows with bad data')
rows_to_delete = dataset[dataset['percipitation'] < 0].index
dataset = dataset.drop(rows_to_delete)
print(f'removed {len(rows_to_delete)} rows bcs of percipitation')

rows_to_delete = dataset[dataset['temperature'] < -20].index
dataset = dataset.drop(rows_to_delete)
print(f'removed {len(rows_to_delete)} rows bcs of temperature')

dataset.to_csv('../datasets/accidents_raw.csv', index=None)
