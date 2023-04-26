
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from pandas import read_csv
from keras.models import load_model
from joblib import load
from sklearn.dummy import DummyRegressor
from datetime import datetime

starttime = datetime.now()


RESCALE_VALUES = True


# load datasets
X_test = read_csv('../datasets/accidents_X_test.csv')
y_test = read_csv('../datasets/accidents_y_test.csv')
X_train = read_csv('../datasets/accidents_X_train.csv')
y_train = read_csv('../datasets/accidents_y_train.csv')
weather_stations = read_csv(
    '../datasets/accidents_weatherstations.csv')

# load models
nn_model = load_model('../models/accidents_model_nn')
rf_model = load('../models/accidents_model_rf.bin')

dummy_model = DummyRegressor(strategy="mean")
dummy_model.fit(X_train, y_train)
# calculate predictions
print("calculating predictions...")
y_pred_nn = nn_model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)
y_pred_dummy = dummy_model.predict(X_test)

if RESCALE_VALUES:
    print("rescaling values...")
    # rescale predictions
    y_test = y_test.to_numpy()
    weather_stations = np.ravel(weather_stations.to_numpy(dtype='int'))

    scalers_dict = {}

    # load scalers
    for weather_station in np.unique(weather_stations):
        scalers_dict[weather_station] = load(
            f'../scalers/accident_scaler_{weather_station}.bin')

    for i in range(len(y_test)):
        y_pred_nn[i] = scalers_dict[weather_stations[i]
                                    ].inverse_transform([y_pred_nn[i]])
        y_pred_rf[i] = scalers_dict[weather_stations[i]
                                    ].inverse_transform([[y_pred_rf[i]]])
        y_pred_dummy[i] = scalers_dict[weather_stations[i]
                                       ].inverse_transform([[y_pred_dummy[i]]])
        y_test[i] = scalers_dict[weather_stations[i]
                                 ].inverse_transform([y_test[i]])

y_test = np.round(y_test)

# mae / mse for neural network
mse_nn = mean_squared_error(y_test, y_pred_nn)
mae_nn = mean_absolute_error(y_test, y_pred_nn)
pd.DataFrame(y_pred_nn).to_csv(
    '../datasets/accidents_y_pred_nn.csv', index=None)

# mae / mse for random forest
mse_rf = mean_squared_error(y_test, y_pred_rf)
mae_rf = mean_absolute_error(y_test, y_pred_rf)
pd.DataFrame(y_pred_rf).to_csv(
    '../datasets/accidents_y_pred_rf.csv', index=None)

# mae / mse for dummy
mse_dummy = mean_squared_error(y_test, y_pred_dummy)
mae_dummy = mean_absolute_error(y_test, y_pred_dummy)
pd.DataFrame(y_pred_dummy).to_csv(
    '../datasets/accidents_y_pred_dummy.csv', index=None)


pd.DataFrame(y_test).to_csv(
    '../datasets/accidents_y_test_rescaled.csv', index=None)

print('Mean squared error from neural network: ', mse_nn)
print('Mean squared error from random forest: ', mse_rf)
print('Mean squared error from dummy model: ', mse_dummy, '\n')
print('Mean absolute error from neural network: ', mae_nn)
print('Mean absolute error from random forest: ', mae_rf)
print('Mean absolute error from dummy model: ', mae_dummy)

# Print feature importance
feature_list = list(X_test.columns)
feature_importances = pd.Series(rf_model.feature_importances_,
                                index=feature_list).sort_values(ascending=False)
print(feature_importances)
print(y_pred_nn[:20])

print(f'Execution Time: {datetime.now() - starttime }')
