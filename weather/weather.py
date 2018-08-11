import sys, requests
from datetime import datetime,timedelta
import pandas as pd

loc = ["47.964718", "7.955852"]

d_from_date = datetime.strptime('2017-10-01' , '%Y-%m-%d')
d_to_date = datetime.strptime('2018-08-10' , '%Y-%m-%d')

delta = d_to_date - d_from_date
latitude = loc[0]
longitude = loc[1]

with open('/home/kh41/02_SolarAnlage/api', 'r') as file:
	for line in file:
		api_key=line.rstrip()


option_list = "exclude=currently,minutely,hourly,alerts&units=si"
df = pd.DataFrame()

print("\nLocation: home")
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
	if'precipProbability' in json_res['daily']['data'][0] and 'precipType' in json_res['daily']['data'][0] and 'cloudCover' in json_res['daily']['data'][0]:
		precip_type = json_res['daily']['data'][0]['precipType']
		cloud_cover = json_res['daily']['data'][0]['cloudCover']
		humidity = json_res['daily']['data'][0]['humidity']
		visibility = json_res['daily']['data'][0]['visibility']
		sunrise = json_res['daily']['data'][0]['sunriseTime']
		sunset = json_res['daily']['data'][0]['sunsetTime']
		precip_prob = json_res['daily']['data'][0]['precipProbability']
		# print("Precip type: {}".format(precip_type))
		# print("cloudCover: {}".format(cloud_cover))
		# print("humidity: {}".format(humidity))
		# print("sunrise: {}".format(datetime.fromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')))
		# print("sunset: {}".format(datetime.fromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')))
	if (precip_type == 'rain' and precip_prob != None):
		# precip_prob *= 100
		pass
		# print("Chance of rain: %.2f%" % (precip_prob))
	else:
		precip_prob = 0
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
df.to_csv('/home/kh41/02_SolarAnlage/weather.csv')


	