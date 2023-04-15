
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from pandas import read_csv
from keras.models import load_model
from joblib import load
# load datasets
X_test = read_csv('../datasets/accidents_small_X_test.csv')
y_test = read_csv('../datasets/accidents_small_y_test.csv')

# load models
nn_model = load_model('../models/accidents_small_model_nn')
# TODO load rf model
rf_model = load('../models/accidents_small_model_rf.bin')


# mae / mse for neural network
mse_nn, mae_nn = nn_model.evaluate(X_test, y_test)
print('Mean squared error from neural network: ', mse_nn)
print('Mean absolute error from neural network: ', mae_nn)

# mae / mse for random forest
y_pred_rf = rf_model.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
mae_rf = mean_absolute_error(y_test, y_pred_rf)
print('Mean squared error from random forest: ', mse_rf)
print('Mean absolute error from random forest: ', mae_rf)

# Print feature importance
feature_list = list(X_test.columns)
feature_importances = pd.Series(rf_model.feature_importances_,
                                index=feature_list).sort_values(ascending=False)
print(feature_importances)
print(feature_importances)
