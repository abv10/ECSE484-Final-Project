from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep 
import sqlite3



def nba_scrape(year):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    draft_path = "https://www.basketball-reference.com/draft/NBA_" + str(year) + ".html"
    driver.get(draft_path)

    sleep(2)

    draft_table = driver.find_element(by=By.ID, value =
        "stats"
    )
    #print(x.text)
    rows  = draft_table.find_elements(By.CSS_SELECTOR, value="tr")
    length = len(rows)
    allrows = []
    for row in rows:
        c = row.get_attribute('class')
        if c == "":
            d = row.find_elements(By.CSS_SELECTOR, value="td")
            data = []
            for di in d:
                data.append(di.text)
            if len(data) > 0:
                allrows.append(data)

    driver.quit()

    player_data = []
    #Get Relevant Data
    for players in allrows:
        try:
            if players[3] == '':
                continue
        except:
            continue
        rel_col = [1,2,3,4,5,6,7,18,19,20,21]
        p = []
        for col in rel_col:
            p.append(players[col-1])
        player_data.append(p)

    for row in range(len(player_data)):
        p_row = player_data[row]
        for p_col in range(len(p_row)):
            if p_col not in [1,2,3]:
                if p_row[p_col] == '':
                    p_row[p_col] = 0.0
                else:
                    p_row[p_col] = float(p_row[p_col]) 
                    #print(str(p_col) + str(p_row[p_col]))
        
        p_row.append(year)
        #print(p_row[0])
        #print(p_row[-1])
        id_n = int(str(int(p_row[0]))+str(p_row[-1]))
        p_row.insert(0, id_n)
        player_data[row] = p_row

    conn = sqlite3.connect('basketball_db.sqlite')
    cur = conn.cursor()
    cur.executemany('INSERT INTO nba VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);', player_data)
    print('We have inserted', cur.rowcount, 'records to the table for .' + str(year))
    conn.commit()

    conn.close()


if __name__ == "__main__":
    for i in range(30):
        nba_scrape(i+2001)