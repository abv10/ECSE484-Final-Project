import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep 
from selenium.common import exceptions


def CollegeStats(name, year, for_id, num):

    name = name.lower()
    name.replace('.','')
    split_name = name.split(" ")
    h_name = split_name[0]+"-"+split_name[1]+"-"
    try:
        driver.get("https://www.sports-reference.com/cbb/players/" + h_name + str(num) + ".html")
        p_name = driver.find_element(By.CLASS_NAME, value="players")
        try:
            draft  = driver.find_element(By.XPATH, value="//p[strong = 'Draft:']")

            driver.maximize_window()
            sleep(0.75)

            if str(year) in draft.text:
                tab = driver.find_element(By.ID, value="players_per_game")
                rows = tab.find_elements(By.CSS_SELECTOR, value="tr")
                car_row = 'None'
                for i in range(9):
                    text = rows[i].find_elements(By.CSS_SELECTOR, value="th")[0].text
                    if text == 'Career':
                        car_row = i
                        break
                         
                years = car_row -1
                data = [for_id, year, years]
                cols = rows[car_row].find_elements(By.CSS_SELECTOR, value="td")
                exclude = [1,2,18,19, 27]
                for col_in in range(len(cols)):
                    if (col_in +1) in exclude:
                        continue
                    elif cols[col_in].text == '':
                        data.append(0.0)
                    else:
                        data.append(float(cols[col_in].text))
                    #print(col.text + ",")
                height = driver.find_element(By.XPATH, value="//span[@itemprop='height']")
                split = height.text.split("-")
                in_inches = int(split[0])*12 + float(split[1])
                try:
                    weight_el = driver.find_element(By.XPATH, value="//span[@itemprop='weight']")
                    weight = weight_el.text
                except:
                    weight = input("Enter your value: ")
                weight = int(weight[:len(weight)-2])
                div  = driver.find_element(By.XPATH, value="//div[@itemtype = 'https://schema.org/Person']")
                position_el = driver.find_elements(By.CSS_SELECTOR, value='p')
                pos_string = position_el[1].text
                position =''
                if("Position" in pos_string):
                    position = pos_string.split(" ")[1]
                else:
                    pos_string = position_el[2].text
                    position = pos_string.split(" ")[1]
                data.append(in_inches)
                data.append(weight)
                data.append(position_to_num(position=position))
                return data
            else:
                print("not" + draft.text)
                raise Exception("not " + draft.text)
        except exceptions.InvalidSessionIdException as e:
            raise e
                
        except Exception as e:
            print("Wrong version of player" + name + str(num) + ": ")
            print(e)
            if num < 10:
                #driver.close()
                return CollegeStats(name, year, for_id, num +1)
            else:
                print("Unable to retrieve value for: " + name + ":" + str(year))
                return "None found"
    except exceptions.InvalidSessionIdException as e:
           raise e
    except Exception as e:
        print(e)
        print("Unable to retrieve value for: " + name + ":" + str(year))
        return "None found"
    finally:
        pass 

def position_to_num(position):
    if position == "Forward":
        return 0.75
    elif position == "Center":
        return 1
    elif position == 'Guard':
        return 0
    else:
        raise Exception("No position found")

if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    conn = sqlite3.connect('basketball_db.sqlite')
    year = 1997
    cur = conn.cursor()

    cur.execute('SELECT id as id, name, year FROM nba WHERE year = {} '.format(year))
    data = cur.fetchall()
    #print(data)
    playerinfo = []
    playersToAddManually = []

    for d in data:
        try:
            info = CollegeStats(d[1], d[2], d[0], 1)
        except exceptions.InvalidSessionIdException as e:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            info = CollegeStats(d[1], d[2], d[0], 1)
        print(info)
        if info == "None found":
            playersToAddManually.append(d[1])
        elif info == None:
            print(d[1])
        else:
            playerinfo.append(info)


    print(playerinfo)
    cur.executemany('INSERT INTO college VALUES(?,?,?,?,?,?,?,?, ?,?,?,?,?,?,?,?,?, ?,?,?,?,?,?,?,?,?,?,?,?);', playerinfo)
    print('We have inserted', cur.rowcount, 'records to the table for .' + str(year))
    print(playersToAddManually)
    f = open(str(year) + ".txt", "w", encoding="utf-8")
    for p in playersToAddManually:
        f.write("%s\n" % p)

    conn.commit()

    driver.quit()

    conn.close()

