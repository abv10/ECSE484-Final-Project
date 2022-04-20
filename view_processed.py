import pandas as pd
import numpy as np
import csv

np.set_printoptions(precision=3)

train = pd.read_csv('processeddata.csv', names=["WS", "ID", "Year", "Years", "G", "GS", "MP", "FG", "FGA",
    "FGPer", "TwoP", "TwoPA", "TwoPAPer", "ThreeP", "ThreePA", "ThreePAPer", "FT", "FTA", "FTPER", "TRB", "Assist", "Steal", "Blk",
    "Turnover", "Fouls", "Points", "SOS", "Height", "Weight", "Position"])

train.head()


features = np.array(train.copy())
for row in features:
    pick = (row[1]-(1990.0+30*row[2])) / 10000
    row[1] = pick


features = features[features[:,0].argsort()]

print(features)