# Scrapeo - Scraping weather forecast data from meteo.ch.


A simple web scraper which extracts daily weather forecast data from the Swiss weather service [Meteo](https://meteo.ch) for the region of [St. Gallen](https://meteo.ch/index.php?pid=29).


### Content and functionality:

- File `meteo.py` runs once per day and generates an updated data set which is
stored in folder `data`. 
- The Python script is triggered automatically using 
either a [cronjob (Linux)](https://amannj.github.io/blog/2021/01/05/cronjobs) or
the [Windows Scheduler (for Windows)](https://amannj.github.io/blog/2020/12/16/windows-scheduler).
- Weather info graphs are stored in folder `pics` for further reference.