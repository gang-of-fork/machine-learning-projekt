# TODO fix imports, save model to /models
from pandas import read_csv
from sklearn.ensemble import RandomForestRegressor
from joblib import dump
from numpy import ravel
from datetime import datetime

starttime = datetime.now()

X_train = read_csv('../datasets/temp/accidents_X_train.csv')
y_train = read_csv('../datasets/temp/accidents_y_train.csv')

model = RandomForestRegressor(n_estimators=64, random_state=30)
model.fit(X_train, ravel(y_train.to_numpy()))

dump(model, '../models/accidents_model_rf.bin')

print(f'Execution Time: {datetime.now() - starttime }')
