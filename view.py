import sqlite3

conn = sqlite3.connect('basketball_db.sqlite')
cur = conn.cursor()

cur.execute(
    'SELECT n.WS, c.* FROM nba n, college c WHERE c.id == n.id'
)


data = cur.fetchall()
print(data[0])
conn.commit()
conn.close()
conn = sqlite3.connect('basketball_db.sqlite')

cursor = conn.cursor()




