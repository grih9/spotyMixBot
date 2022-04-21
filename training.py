import csv

import tensorflow as tf
from keras.models import Sequential
from keras import initializers
from keras import optimizers
from keras.layers import *
import pandas as pd
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

import numpy as np
from sklearn.preprocessing import MinMaxScaler

from pr_constants import GNI, G


def load_dataset():
    # labels = np.array(GNI)
    # labels = labels.reshape(labels.shape[0], 1)

    train_data = pd.read_csv("train_data.csv")
    train_features = train_data[["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness",
                                "liveness", "valence", "tempo", "id"]].reset_index(drop=True)
    train_genres = train_data[["genre"]].reset_index(drop=True)
    names = train_features[["id"]].reset_index(drop=True)
    scaler = MinMaxScaler()
    pop_scaled = pd.DataFrame(scaler.fit_transform(train_features), columns=train_features.columns)
    pop_scaled.head()
    train_features = pop_scaled

    labels = train_genres

    # print(labels)

    train_x, test_x, train_y, test_y = train_test_split(train_features, labels, test_size=0.1)

    # print(set(train_y).difference(set(test_y)))
    train_y = np_utils.to_categorical(train_y)
    test_y = np_utils.to_categorical(test_y)
    # n_classes = len(genre)
    # genre_new = {value: key for key, value in genre.items()}

    return train_x, test_x, train_y, test_y


train_x, test_x, train_y, test_y = load_dataset()
print(train_x.shape)
print(test_x.shape)
print(train_y.shape)
print(test_y.shape)

# train_x = train_x.reshape(train_x.shape[0], train_x.shape[1], 1)
# test_x = test_x.reshape(test_x.shape[0], test_x.shape[1], 1)

model = Sequential()
model.add(Flatten(input_shape=[9]))
model.add(Dropout(0.6))
model.add(Dense(1024, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(256, activation="relu"))
model.add(Dropout(0.25))
model.add(Dense(64, activation="relu"))
model.add(Dense(32, activation="relu"))
model.add(Dense(len(G), activation="softmax"))
model.compile(loss="categorical_crossentropy", optimizer=tf.optimizers.Adam(lr=0.0001), metrics=['accuracy'])
print(model.summary())
pd.DataFrame(model.fit(train_x, train_y, epochs=10, verbose=1, validation_split=0.1).history).to_csv("training_history.csv")
score = model.evaluate(test_x, test_y, verbose=1)
print(score)
model.save("Model3.h5")

