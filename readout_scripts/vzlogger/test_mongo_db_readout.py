import pandas as pd
import subprocess
from pymongo import MongoClient
import re

# Choose the appropriate client
client = MongoClient()

# Connect to the db solarAnlage
db = client.solarAnlage

# Use the collection vzlogger
vzlogger = db.vzlogger

# Bulk inserting documents. Each row in the DataFrame will be a document in Mongo
# coll.insert_many(data.to_dict('records'))


# ====== Finding Documents ====== #
documents = vzlogger.find()
data = pd.DataFrame(list(documents))
print(data)

ts = data['time'].values[-1]
time_string = str(ts.year)+'-'+str(ts.month)+'-'+str(ts.day)

data.to_csv(time_string+'latest_vzlogger_reading.csv')