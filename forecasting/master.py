# 001_darkSky_weatherData.py
# 002_extractSunHours.py
# 003_sunData.py
import pandas as pd

from darkSky_weatherData import getDarkSkyWeatherData
from sunData import getSunData

loc = ["47.964718", "7.955852"]

startDate = '2017-10-01'
endDate = '2018-08-11'
# endDate = '2017-10-11'

# connect to API and get weather data for location loc, interval is days
df = getDarkSkyWeatherData(loc, startDate, endDate)
fname = '/home/kh41/02_SolarAnlage/weather.csv'
df.to_csv(fname)

# get data from pysolar about altitude, azimuth and calculated irradiation when the sun is at max altitude at that day
df = getSunData(loc, df)

fname = '/home/kh41/02_SolarAnlage/weather.csv'
df.to_csv(fname)

