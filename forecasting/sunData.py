from pysolar.solar import *
import datetime
import numpy as np
import pandas as pd
pd.set_option("display.max_rows",101)
pd.set_option("display.max_columns",101)

# fname = '/home/kh41/02_SolarAnlage/weather.csv'
# df = pd.read_csv(fname, index_col=0)
# df = df.drop(columns=['0'])

# # location of home
# loc = [47.964718, 7.955852]

def getSunData(loc, df):
	loc = [float(loc[0]), float(loc[1])]
	# date = datetime.datetime.strptime('2018-08-12 14:00:00', '%Y-%m-%d %H:%M:%S')
	# Then, use the solar.get_altitude() function to calculate the angle between the sun and a plane tangent to the earth where you are. The result is returned in degrees.:
	# http://pysolar.readthedocs.io/en/latest/#examples
	# get the maximum altitude for one day
	def getMaxAltitude(df):
		date = df['date']
		day = datetime.datetime.strptime(date, '%Y-%m-%d %A').date()
		# day = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()
		# print(day)
		times = pd.date_range(day,periods=24,freq='H')
		my_df = pd.DataFrame(times)
		my_df.columns = ['times']
		my_df['time_str'] = my_df['times'].dt.strftime('%Y-%m-%d %H:%M:%S')
		my_df['times'] = pd.to_datetime(my_df['time_str'], format='%Y-%m-%d %H:%M:%S')
		my_df['altitude'] = my_df['times'].apply(lambda x: get_altitude(loc[0], loc[1], x))
		# my_df['altitude'] = get_altitude(loc[0],loc[1],my_df['times'])
		# sun data
		time_max = my_df['time_str'][ my_df['altitude'] == np.max(my_df['altitude']) ].values[0]
		
		altitude_max = my_df.altitude[my_df.altitude == np.max(my_df.altitude)].values[0]

		time_max_dt = datetime.datetime.strptime(time_max, '%Y-%m-%d %H:%M:%S')
		azi = get_azimuth(loc[0],loc[1],time_max_dt)
		irrad = radiation.get_radiation_direct(time_max_dt, altitude_max)

		df['sun_time_altitude_max'] = time_max
		df['sun_altitude_max'] = altitude_max
		df['sun_azimuth'] = azi  # when the altitude was max
		df['sun_irradiation'] = irrad  # when the altitude was max

		return df

	# alti = get_altitude(loc[0], loc[1], date)
	# azi = get_azimuth(loc[0],loc[1],date)
	# irrad = radiation.get_radiation_direct(date, alti)
	# print(alti, azi, irrad)

	# print(getMaxAltitude('2018-08-12 14:00:00'))

	df = df.apply(lambda x: getMaxAltitude(x), axis=1)

	return df

# fname = '/home/kh41/02_SolarAnlage/weather.csv'
# df.to_csv(fname)