import matplotlib.pyplot as plt
from pandas import read_csv

dataset = read_csv('../datasets/accidents_raw.csv')

print(dataset.corr())

print("accidents distributions")
fig, ax = plt.subplots()
ax.set_xlabel('Anzahl der Unfälle')
ax.set_ylabel('Anzahl der Datenpunkte')
dataset['accidents'].value_counts().plot.bar()
plt.show()


print('grouped plots')
for column in ['hour', 'day', 'month']:
    dataset.boxplot(column='accidents', by=column)
    dataset_grouped_by_hour = dataset.groupby([column]).mean().reset_index()
    x = dataset_grouped_by_hour[column]
    y = dataset_grouped_by_hour['accidents']
    fig, ax = plt.subplots()
    ax.set_xlabel(column)
    ax.set_ylabel('accidents')
    ax.scatter(x, y)
    ax.plot(x, y)
    plt.show()


print('ungrouped plots')


for column in ['percipitation', 'road_usage', 'temperature']:

    dataset_grouped_by_hour = dataset.groupby([column]).mean().reset_index()

    x = dataset_grouped_by_hour[column]
    y = dataset_grouped_by_hour['accidents']

    fig, ax = plt.subplots()
    ax.set_xlabel(column)
    ax.set_ylabel('accidents')
    ax.scatter(x, y)
    plt.show()
