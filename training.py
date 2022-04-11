import csv

import tensorflow as tf
from keras.models import Sequential
from keras import initializers
from keras import optimizers
#from keras.utils import plot_model
from keras.layers import *
import pandas as pd
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

import numpy as np

from pr_constants import GNI, G


def load_dataset():
    # labels = np.array(GNI)
    # labels = labels.reshape(labels.shape[0], 1)
    tmp_dict = dict()

    with open("train_data.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        data = []
        labels = []
        flag = False
        for row in csv_reader:
            if not flag:
                flag = True
                continue

            # if tmp_dict.get(GNI[row[9]]) is None:
            #     tmp_dict[GNI[row[9]]] = 1
            # else:
            #     tmp_dict[GNI[row[9]]] += 1
            #
            # if tmp_dict[GNI[row[9]]] >= 10000:
            #     print(GNI[row[9]], tmp_dict[GNI[row[9]]])
            #     continue

            labels.append(GNI[row[9]])
            tmp = list(map(float, row[:8]))
            tmp[2] /= -60.0
            data.append(tmp)

    # print(labels)

    train_x, test_x, train_y, test_y = train_test_split(np.array(data), np.array(labels), test_size=0.1)

    # Convert the labels into one-hot vectors.
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
# datasetSize = 0.75, this returns 3/4th of the dataset.

# Expand the dimensions of the image to have a channel dimension. (nx128x128) ==> (nx128x128x1)

# train_x = train_x.reshape(train_x.shape[0], train_x.shape[1], 1)
# test_x = test_x.reshape(test_x.shape[0], test_x.shape[1], 1)

model = Sequential()
model.add(Flatten(input_shape=[8]))
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
#plot_model(model, to_file="Saved_Model/Model_Architecture.jpg")
pd.DataFrame(model.fit(train_x, train_y, epochs=10, verbose=1, validation_split=0.1).history).to_csv("training_history.csv")
score = model.evaluate(test_x, test_y, verbose=1)
print(score)
model.save("Model2.h5")

