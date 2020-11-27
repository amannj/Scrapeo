import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import re


# Date
todaysDate = datetime.datetime.today();
todaysDate = todaysDate.strftime("%Y-%m-%d %H:%M")


# Scrape data
URL_today  = 'https://meteo.ch/index.php?pid=29'
page_today = requests.get(URL_today)
soup_today = BeautifulSoup(page_today.content, 'html.parser')


# Extract weather information today
weather_today = soup_today.find('table', class_='ortswetter').text
t_today       = re.findall("[0-9]*", weather_today)
t_today       = [x for x in t_today if x != '']
n_today       = weather_today[14:]
n_today       = re.findall(".+?(?=\\\n)", n_today)[0]


# Weather symbols
sym_list = []
for sym in soup_today.find_all('img', class_ = "symbol"):
    sym_list.append(sym.get('src')[8:])


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
df_old = pd.read_csv('data/StGallen.csv')
df_new = df_old.append(df)
## Save
df_new.to_csv('data/StGallen.csv', index = False)