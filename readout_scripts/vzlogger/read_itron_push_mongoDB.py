import pandas as pd
import subprocess
from pymongo import MongoClient
import re

# read the vzlogger
def read_vzlogger(collection):
	# collection: collection to use to store the document
	# return: dictionary with time, OBIS identifiers 1.8.0, 2.8.0, and respective values

	# initialize output dictionary
	out = {'time': 0, '1-8-0': 0, '2-8-0': 0}

	# get current time
	time = pd.Timestamp.now()

	# start vzlogger script
	cmd = 'vzlogger'
	res = subprocess.run([cmd], stdout=subprocess.PIPE).stdout.decode('utf-8')
	res = res.split(' ')

	# capture the relevant output and add to dictionary
	for ii in range(0,len(res)):
		item = res[ii]
		_ = re.findall(r'ObisIdentifier:1-0:(.*)\*255', item)
		if len(_) > 0:
			ID = _[0] # OBIS Identifier
			val = re.findall(r'value=(.*)', res[ii+1])[0]  # value in Wh
			assert len(val) > 0
			val = float(val)
			assert ID in ['1.8.0', '2.8.0']
			if ID == '1.8.0':
				out['1-8-0'] = val
			if ID == '2.8.0':
				out['2-8-0'] = val
			# print(item, res[ii+1])  # print the line and value raw

	out['time'] = time

	# return
	return out

# Choose the appropriate client
client = MongoClient()

# Connect to the db solarAnlage
db = client.solarAnlage

# Use the collection vzlogger
vzlogger = db.vzlogger

data = read_vzlogger(vzlogger)
print(data)

df = pd.DataFrame(data, index=0)

# Bulk inserting documents. Each row in the DataFrame will be a document in Mongo
vzlogger.insert_many(df.to_dict('records'))

