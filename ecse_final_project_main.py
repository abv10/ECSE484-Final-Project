# -*- coding: utf-8 -*-
"""ECSEFinalProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10NSf7_j8VUN6nt7E3JE146QkcXmdOew1
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Make numpy values easier to read.
np.set_printoptions(precision=3)

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import losses
from tensorflow.keras import *


data = pd.read_csv('processeddata.csv', names=["WS", "ID", "Year", "Years", "G", "GS", "MP", "FG", "FGA",
        "FGPer", "TwoP", "TwoPA", "TwoPAPer", "ThreeP", "ThreePA", "ThreePAPer", "FT", "FTA", "FTPER", "TRB", "Assist", "Steal", "Blk",
        "Turnover", "Fouls", "Points", "SOS", "Height", "Weight", "Position"])

data.head()


train = data.copy()
train = train.sample(frac=1) #shuffle the order
val = train[-275:]
train = train[:-275]

features = train.copy()
labels = features.pop("WS")
features.pop("ID")

val_features = val.sort_values(by="WS")
sorted = val_features.copy()
val_labels = val_features.pop("WS")
val_features.pop("ID")
print(val_labels)

features = np.array(features)
val_features = np.array(val_features)

def plot_loss(history):
  plt.plot(history.history['loss'], label='loss')
  plt.plot(history.history['val_loss'], label='val_loss')
  plt.ylim([0, 0.2])
  plt.xlabel('Epoch')
  plt.ylabel('Error [Abs]')
  plt.legend()
  plt.grid(True)

model = tf.keras.Sequential([
  layers.Dense(29, activation=activations.linear),
  layers.Dense(14, activation=activations.relu),
  layers.Dense(14, activation=activations.linear),
  layers.Dense(14, activation=activations.relu),
  layers.Dense(14, activation=activations.linear),
  layers.Dense(14, activation=activations.relu),
  layers.Dense(14, activation=activations.relu),
  layers.Dense(units=1, activation=activations.linear)
])

model.compile(loss = tf.keras.losses.MeanAbsoluteError(),
                      optimizer = tf.optimizers.Adam())

history = model.fit(features, labels, batch_size = 100, epochs=200, validation_data=(val_features, val_labels))
model.summary()
plot_loss(history)



predicted_ws = np.transpose(np.array(model.predict(val_features)))
predicted_ws = predicted_ws[0]
actual_ws = np.transpose(np.array(val_labels))

plt.scatter(predicted_ws, actual_ws)

z = np.polyfit(predicted_ws, actual_ws, 1)
p = np.poly1d(z)
print(p)
plt.plot(predicted_ws,p(predicted_ws),"r--")

plt.xlabel('Predicted Normalized')
plt.ylabel('Actual Normalized')

picks = np.array(sorted)
sorted_picks = []
for row in picks:
    pick = (row[1]-(1990.0+30*row[2])) / 10000
    sorted_picks.append((60 - pick)/60)


plt.scatter(sorted_picks, actual_ws)
z = np.polyfit(sorted_picks, actual_ws, 1)

p = np.poly1d(z)
draft_slope = z[0]
draft_yintercept = z[1]
plt.plot(sorted_picks,p(sorted_picks),"r--")

import sys
import math
import csv

val_norm = .0772

max = 13.76
min = -0.34

print((val_norm * (max - min) + min))
np.set_printoptions(precision=3, threshold=sys.maxsize)

dis_play = [["Name", "Pick", "WS/Y", "WS/DP", "WS/NN"]]
sorted_arr = np.array(sorted)
names = list(sorted.index)

for row in range(len(sorted_arr)):
  r = []
  r.append(names[row])
  r.append((sorted_arr[row][1]-(1990.0+30*sorted_arr[row][2]))/10000) #Pick
  r.append(math.floor((sorted_arr[row][0]*(max-min)+min)*100)/100) #WS
  pro_by_draft = (60-r[1]) * draft_slope + draft_yintercept
  r.append(math.floor((pro_by_draft)*100)/100) #ProWinShares
  r.append(math.floor((predicted_ws[row] * (max -min) + min)*100)/100) #ProNNWinShares
  dis_play.append(r)

w_o_headers = dis_play[1:]
a = np.array(w_o_headers, dtype=object)


b = a[a[:,4].argsort()]
print(["Name", "Pick", "WS/Y", "WS/DP", "WS/NN"])
print(b)
with open('results.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for row in b:
            writer.writerow(row)