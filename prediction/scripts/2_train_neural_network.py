#!/usr/bin/env python
from matplotlib import pyplot as plt
from pandas import read_csv
from keras.models import Sequential
from keras.callbacks import CSVLogger
from keras.layers import Dense
from keras.metrics import MeanAbsoluteError
from keras.optimizers import Adam


# load datasets
X_train = read_csv('../datasets/temp/accidents_small_X_train.csv')
y_train = read_csv('../datasets/temp/accidents_small_y_train.csv')

# Sequential Model with 3 Hidden Layers and relu activation
model = Sequential()
model.add(Dense(32, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
# Output layer
model.add(Dense(1, activation='linear'))

model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.0003),
              metrics=[MeanAbsoluteError()])
model.summary()

# log the history csv
csv_logger = CSVLogger(
    '../models/accidents_small_history.csv', separator=',', append=False)

# train the model
history = model.fit(X_train, y_train,
                    validation_split=0.2, epochs=50, batch_size=64, callbacks=[csv_logger])


# save the model to a file
model.save('../models/accidents_small_model_nn')


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
