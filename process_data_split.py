import sqlite3
import pandas as pd
import numpy as np
import csv
#(64.3, 11990, 1990, 4, 143.0, 139.0, 32.8, 5.4, 9.5, 0.568, 5.3, 9.1, 0.58,
#  0.1, 0.4, 0.291, 4.1, 6.0, 0.684, 10.7, 2.3, 1.3, 2.2, 2.3, 3.0, 15.0, 8.71, 82, 230, 0.75)

WS = 0
ID = 1
YEAR = 2

def getMaxAndMin(data):
    min_and_max = [[],[]]
    for col in range(len(data[0])):
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
        'SELECT n.WS, c.* FROM nba n, college c WHERE c.id == n.id AND weight > 2 AND c.year % 5 == 0'
    )

    v_data = cur.fetchall()

    cur.execute(
        'SELECT n.WS, c.* FROM nba n, college c WHERE c.id == n.id AND weight > 2 AND c.year % 5 != 0'
    )

    t_data = cur.fetchall()

    print(len(t_data))
    print(len(v_data))

    for i in range(len(v_data)):
        v_data[i] = list(v_data[i])

    for row in v_data:
        year = row[YEAR]
        pre_ws = row[WS]
        row[WS] = pre_ws / min(15, 2022-year)

    min_and_max = getMaxAndMin(v_data)

    processed_validation_data = process(v_data, min_and_max, [ID] )

    with open('validation_data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for row in processed_validation_data:
            writer.writerow(row)

    ####
    for i in range(len(t_data)):
        t_data[i] = list(t_data[i])

    for row in t_data:
        year = row[YEAR]
        pre_ws = row[WS]
        row[WS] = pre_ws / min(15, 2022-year)

    min_and_max = getMaxAndMin(t_data)

    processed_training_data = process(t_data, min_and_max, [ID] )

    with open('training_data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        for row in processed_training_data:
            writer.writerow(row)