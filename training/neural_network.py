#!/usr/bin/env python
from matplotlib import pyplot as plt
from pandas import read_csv
from keras.models import Sequential
from keras.callbacks import CSVLogger
from keras.layers import Dense
from keras.metrics import MeanAbsoluteError
from sklearn.model_selection import train_test_split

# load prepared dataset
df = read_csv("../datasets/accidents_small.csv",
              delimiter=',')

print(df.describe())

# Split into variables and target
X = df.drop('Anzahl_Unfälle', axis=1)
y = df['Anzahl_Unfälle']

# Split into train and test dataset and save to csv
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2)

X_train.to_csv("../datasets/accidents_small_X_train.csv")
X_test.to_csv("../datasets/accidents_small_X_test.csv")
y_train.to_csv("../datasets/accidents_small_y_train.csv")
y_test.to_csv("../datasets/accidents_small_y_test.csv")

# Sequential Model with 3 Hidden Layers and relu activation
model = Sequential()
model.add(Dense(32, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
# Output layer
model.add(Dense(1, activation='linear'))

model.compile(loss='mean_squared_error', optimizer='adam',
              metrics=[MeanAbsoluteError()])
model.summary()

# log the history csv
csv_logger = CSVLogger(
    '../models/accidents_small_history.csv', separator=',', append=False)

# train the model
history = model.fit(X_train, y_train,
                    validation_split=0.2, epochs=50, batch_size=32, callbacks=[csv_logger])


# save the model to a file
model.save('../models/accidents_small_model')


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
