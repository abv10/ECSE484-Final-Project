import sqlite3

conn = sqlite3.connect('basketball_db.sqlite')
cur = conn.cursor()

# cur.execute(
#     '''CREATE TABLE nba 
#     (id INTEGER PRIMARY KEY,
#     pick REAL,
#     team VARCHAR(4) NOT NULL,
#     name VARCHAR(100) NOT NULL,
#     school VARCHAR(30) NOT NULL,
#     years REAL,
#     games REAL,
#     minutes REAL, 
#     WS REAL,
#     WSper REAL, 
#     BPM REAL,
#     VORP REAL,
#     year INTEGER)
#     '''
# )
cur.execute('DROP TABLE college')
cur.execute(
    '''CREATE TABLE college 
    (id INTEGER,
    Year INTEGER,
    Years INTEGER,
    G REAL,
    GS REAL,
    MP REAL,
    FG REAL,
    FGA REAL,
    FGPer REAL,
    TwoP REAL,
    TwoPA REAL,
    TwoPAPer REAL,
    ThreeP REAL,
    ThreePA REAL,
    ThreePAper REAL,
    FT REAL,
    FTA REAL,
    FTPER REAL,
    TRB REAL,
    Assist REAL,
    Steal REAL,
    BLK REAL,
    Turnover REAL,
    Fouls REAL,
    Points REAL,
    SOS REAL,
    Height INTEGER,
    Weight INTEGER,
    Position REAL,
    FOREIGN KEY (id) REFERENCES nba(id))
    '''
)
conn.commit()
conn.close()