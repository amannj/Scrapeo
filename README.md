# Scrapeo - Scraping weather forecast data from meteo.ch?


A simple web scraper which extracts daily weather data (actual plus the 4-day forecasts) from the Swiss weather service [Meteo](https://meteo.ch) for the region of St. Gallen.

File `meteo.py` runs once per day and generates an updated data set which is
stored in folder `data`. The script is triggered automatically.
