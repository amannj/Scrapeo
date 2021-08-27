import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import re
import time


def meteo_extract(loc_name): 

    #
    # Extract weather forecasts; all location data from 'meteo.ch'.
    #

    # Location IDs
    ls_locs = {
        'loc_name': ['StGallen', 'Zuerich', 'Bern', 'Basel', 'Genf', 'Brig', 'Chur', 'Locarno', 'Luzern'],
        'loc_id'  : ['29', '20', '23', '24', '25', '26', '27', '28', '30']
        } 
    df_locs = pd.DataFrame(data=ls_locs)
    loc_id = df_locs[df_locs["loc_name"] == loc_name].iat[0,1]


    # Date
    todaysDate = datetime.datetime.today();
    todaysDate = todaysDate.strftime("%Y-%m-%d %H:%M")


    # Scrape data
    URL_today  = 'https://meteo.ch/index.php?pid='+loc_id
    page_today = requests.get(URL_today)
    soup_today = BeautifulSoup(page_today.content, 'html.parser')


    # Extract weather information today
    weather_today = soup_today.find('table', class_='ortswetter').text
    t_today       = re.findall("[0-9]*", weather_today)
    t_today       = [x for x in t_today if x != '']
    n_today       = re.findall(".+?(?=\\\n)", weather_today)[1]


    # Weather symbols
    sym_list = [
        sym.get('src')[8:]
        for sym in soup_today.find_all('img', class_ = "symbol")
    ]


    # Daily weather forecasts
    ## Temperature
    t_list = t_today
    for sym in soup_today.find_all('div', class_ = ("tx", "tn")):
        t_list.append(sym.string)
    ## Names
    n_list = [n_today]
    for sym in soup_today.find_all('td')[6:11]:
        tmp = sym.text
        n_list.append(re.sub("Montag|Dienstag|Mittwoch|Donnerstag|Freitag|Samstag|Sonntag", "", tmp))


    # Build data
    ## Assemble
    d = {
        'date': [todaysDate] * 5,
        'type': ['today', '1-day fc', '2-day fc', '3-day fc', '4-day fc'],
        'desc': n_list,
        'tx'  : t_today[::2] ,
        'tn'  : t_today[1::2],
        'sym' : sym_list
        }
    df = pd.DataFrame(data=d)
    ## Append
    loc = 'data/'+loc_name+'.csv'
    df_old = pd.read_csv(loc)
    df_new = df_old.append(df)
    ## Save
    df_new.to_csv(loc, index = False)

    # Sleep for 3 seconds
    print(loc_name + ' done.')
    time.sleep(3)


# Extract data
locations = ["Basel", "Bern", "Brig", "Chur", "Genf", "Locarno", "Luzern","StGallen", "Zuerich"]
for x in locations:
    meteo_extract(loc_name = x)