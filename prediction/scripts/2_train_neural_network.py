#!/usr/bin/env python
from matplotlib import pyplot as plt
from pandas import read_csv
from keras.models import Sequential
from keras.callbacks import CSVLogger, EarlyStopping
from keras.layers import Dense
from keras.metrics import MeanAbsoluteError
from keras.optimizers import Adam
import keras_tuner as kt
from datetime import datetime

starttime = datetime.now()


# load datasets
X_train = read_csv('../datasets/accidents_X_train.csv')
y_train = read_csv('../datasets/accidents_y_train.csv')

# define Hypermodel


def build_model(hp):
    # Sequential Model with 2 Hidden Layers and relu activation
    model = Sequential()
    model.add(Dense(hp.Int('units_0', min_value=16, max_value=64,
              step=16), input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(hp.Int('units_1', min_value=16, max_value=64,
              step=32), activation='relu'))
    # Output layer
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.0001),
                  metrics=[MeanAbsoluteError()])
    return model
# model.summary()


tuner = kt.Hyperband(build_model,
                     objective='val_loss',
                     max_epochs=25,
                     factor=3,
                     directory='../models',
                     project_name='acc_avoid_tuning'
                     )

stop_early = EarlyStopping(monitor='val_loss', patience=5)

tuner.search(X_train, y_train, epochs=50,
             validation_split=0.2, callbacks=[stop_early])

best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
print(f"""
The hyperparameter search is complete. The optimal number of units in the first densely-connected
layer is {best_hps.get('units_0')} and 2nd layer {best_hps.get('units_1')}.
""")
model = tuner.hypermodel.build(best_hps)

# train the model
history = model.fit(X_train, y_train,
                    validation_split=0.2, epochs=50, batch_size=64)


# save the model to a file
model.save('../models/accidents_model_nn')


# plot the training and validation accuracy and loss at each epoch
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'y', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()


acc = history.history['mean_absolute_error']
val_acc = history.history['val_mean_absolute_error']
plt.plot(epochs, acc, 'y', label='Training MAE')
plt.plot(epochs, val_acc, 'r', label='Validation MAE')
plt.title('Training and validation MAE')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()


print(f'Execution Time: {datetime.now() - starttime }')
