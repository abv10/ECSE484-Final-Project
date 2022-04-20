import sqlite3
import pandas as pd
import numpy as np
import csv
#(64.3, 11990, 1990, 4, 143.0, 139.0, 32.8, 5.4, 9.5, 0.568, 5.3, 9.1, 0.58,
#  0.1, 0.4, 0.291, 4.1, 6.0, 0.684, 10.7, 2.3, 1.3, 2.2, 2.3, 3.0, 15.0, 8.71, 82, 230, 0.75)

NAME = 0
WS = 1
ID = 2
YEAR = 3

def getMaxAndMin(data, exclude=[]):
    min_and_max = [[],[]]
    for col in range(len(data[0])):
        if col in exclude:
            min_and_max[0].append(None)
            min_and_max[1].append(None)

            continue
        min = 100000
        max = -1000000
        for row in range(len(data)):
            val = data[row][col]
            if(val < min):
                min = val
            if (val > max):
                max = val
        min_and_max[0].append(min)
        min_and_max[1].append(max)
    return min_and_max

def process(data, min_and_max, exclude=[]):
    for col in range(len(data[0])):
        if col in exclude:
            continue

        min = min_and_max[0][col]
        max = min_and_max[1][col]
        for row in range(len(data)):
            val = data[row][col]
            data[row][col] = (val - min) / (max - min)
            
    return data


if __name__ == "__main__":
    np.set_printoptions(precision=3, suppress=True)
    conn = sqlite3.connect('basketball_db.sqlite')
    cur = conn.cursor()

    
    cur.execute(
        'SELECT n.name, n.WS, c.* FROM nba n, college c WHERE c.id == n.id AND weight > 2'
    )

    data = cur.fetchall()
    for i in range(len(data)):
        data[i] = list(data[i])

    print(data[0])
    for row in data:
        year = row[YEAR]
        pre_ws = row[WS]
        row[WS] = pre_ws / min(15, 2022-year)

    min_and_max = getMaxAndMin(data, [ID, NAME])
    print(min_and_max[0][1])
    print(min_and_max[1][1])

    processed_data = process(data, min_and_max, [ID, NAME] )

    with open('processeddata.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for row in processed_data:
            writer.writerow(row)

    train = pd.read_csv('processeddata.csv', names=["WS", "ID", "Year", "Years", "G", "GS", "MP", "FG", "FGA",
        "FGPer", "TwoP", "TwoPA", "TwoPAPer", "ThreeP", "ThreePA", "ThreePAPer", "FT", "FTA", "FTPER", "TRB", "Assist", "Steal", "Blk",
        "Turnover", "Fouls", "Points", "SOS", "Height", "Weight", "Position"])

    train.head()

    features = train.copy()
    labels = train.pop("WS")

    features = np.array(features)
    
