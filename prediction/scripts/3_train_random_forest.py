# TODO fix imports, save model to /models
from pandas import read_csv
from sklearn.ensemble import RandomForestRegressor
from joblib import dump
from numpy import ravel

X_train = read_csv('../datasets/accidents_small_X_train.csv')
y_train = read_csv('../datasets/accidents_small_y_train.csv')

model = RandomForestRegressor(n_estimators=128, random_state=30)
model.fit(X_train, ravel(y_train.to_numpy()))

dump(model, '../models/accidents_small_model_rf.bin')