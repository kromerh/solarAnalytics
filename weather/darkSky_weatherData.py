import sys, requests
from datetime import datetime,timedelta
import pandas as pd

# loc = ["47.964718", "7.955852"]

# startDate = '2017-10-01'
# endDate = '2018-08-11'

def getDarkSkyWeatherData(loc, startDate, endDate):

	d_from_date = datetime.strptime(startDate, '%Y-%m-%d')
	d_to_date = datetime.strptime(endDate , '%Y-%m-%d')


	delta = d_to_date - d_from_date
	latitude = loc[0]
	longitude = loc[1]

	with open('/home/kh41/02_SolarAnlage/api', 'r') as file:
		for line in file:
			api_key=line.rstrip()


	option_list = "exclude=currently,minutely,hourly,alerts&units=si"
	df = pd.DataFrame()

	print("\nLocation: {}, {}".format(loc[0], loc[1]))
	for i in range(delta.days+1):
		my_df = pd.DataFrame([0])
		
		new_date = (d_from_date + timedelta(days=i)).strftime('%Y-%m-%d')
		search_date = new_date+"T00:00:00"
		response = requests.get("https://api.darksky.net/forecast/"+api_key+"/"+latitude+","+longitude+","+search_date+"?"+option_list)
		json_res = response.json()
		
		date_id = (d_from_date + timedelta(days=i)).strftime('%Y-%m-%d %A')

		my_df['date'] = date_id

		print("\n"+date_id)
		unit_type = ' degC' 
		temp_min = str(json_res['daily']['data'][0]['apparentTemperatureMin'])
		temp_max = str(json_res['daily']['data'][0]['apparentTemperatureMax'])

		# print("Min temperature: "+temp_min+unit_type)
		# print("Max temperature: "+temp_max+unit_type)
		# print("Summary: " + json_res['daily']['data'][0]['summary'])
		precip_type = None
		precip_prob = None
		try:
			precip_type = json_res['daily']['data'][0]['precipType']
		except:
			precip_type = -1
		try:
			cloud_cover = json_res['daily']['data'][0]['cloudCover']
		except:
			cloud_cover = -1
		try:
			humidity = json_res['daily']['data'][0]['humidity']
		except:
			humidity = -1

		# visibility = json_res['daily']['data'][0]['visibility']
		sunrise = json_res['daily']['data'][0]['sunriseTime']
		sunset = json_res['daily']['data'][0]['sunsetTime']
		try:
			precip_prob = json_res['daily']['data'][0]['precipProbability']
		except:
			precip_prob = -1
			# print("Precip type: {}".format(precip_type))
			# print("cloudCover: {}".format(cloud_cover))
			# print("humidity: {}".format(humidity))
			# print("sunrise: {}".format(datetime.fromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')))
			# print("sunset: {}".format(datetime.fromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')))

		# except:
		# 	precip_type = -1
		# 	cloud_cover = -1
		# 	humidity = -1
		# 	sunrise = -1
		# 	sunset = -1
		# 	precip_prob = -1
		my_df['precip_type'] = precip_type
		my_df['precip_prob'] = precip_prob
		my_df['cloud_cover'] = cloud_cover
		my_df['humidity'] = humidity
		my_df['sunrise'] = datetime.fromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')
		my_df['sunset'] = datetime.fromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')
		my_df['longitude'] = longitude
		my_df['latitude'] = latitude
		# print(my_df.head())
		df = df.append(my_df)

	df = df.reset_index(drop=True)
	df = df.drop(columns=[0])  # there is a 0 column remaining

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
	# df.to_csv('/home/kh41/02_SolarAnlage/weather.csv')

	return df


	