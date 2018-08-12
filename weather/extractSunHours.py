import sys, requests
from datetime import datetime,timedelta
import pandas as pd

fname = '/home/kh41/02_SolarAnlage/weather.csv'
df = pd.read_csv(fname, index_col=0)
df = df.drop(columns=['0'])

# calculate sun uptime in seconds
def getSunTime(sunrise, sunset):
	sunset = datetime.strptime(sunset, '%Y-%m-%d %H:%M:%S')
	sunrise = datetime.strptime(sunrise, '%Y-%m-%d %H:%M:%S')
	# print(sunset, sunrise)
	sun_time = (sunset - sunrise).seconds 
	# print(sun_time)
	# sys.exit()
	return sun_time
	
df['sun_time'] = df.apply(lambda x: getSunTime(x['sunrise'], x['sunset']), axis=1)
print(df)