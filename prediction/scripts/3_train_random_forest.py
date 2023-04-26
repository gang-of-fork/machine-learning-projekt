# TODO fix imports, save model to /models
from pandas import read_csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from joblib import dump
from numpy import ravel
from datetime import datetime

starttime = datetime.now()

X_train = read_csv('../datasets/accidents_X_train.csv')
y_train = read_csv('../datasets/accidents_y_train.csv')

param_grid = {
    'n_estimators': [32, 64, 128, 256, 512],
    'max_depth': [4, 6, 8, 10]
}

GridSearchRandomForest = GridSearchCV(RandomForestRegressor(
    random_state=42), param_grid=param_grid, cv=5, scoring='neg_mean_squared_error')
GridSearchRandomForest.fit(X_train, ravel(y_train.to_numpy()))

print('Grid Search for Random Forest is complete. Best params are:')
print(GridSearchRandomForest.best_params_)
print('Score was:')
print(GridSearchRandomForest.best_score_)
print(GridSearchRandomForest.cv_results_)

model = RandomForestRegressor(n_estimators=GridSearchRandomForest.best_params_[
                              'n_estimators'], max_depth=GridSearchRandomForest.best_params_['max_depth'], random_state=30)
model.fit(X_train, ravel(y_train.to_numpy()))

dump(model, '../models/accidents_model_rf.bin')

print(f'Execution Time: {datetime.now() - starttime }')
