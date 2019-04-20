from pymongo import MongoClient
import pandas as pd
import numpy as np
import datetime

# Choose the appropriate client
client = MongoClient()

# Connect to the db solarAnlage
db = client.solarAnlage

# Use the collection vzlogger
vzlogger = db.vzlogger

# ====== Inserting Documents ====== #
# Creating a simple Pandas DataFrame
time = pd.Timestamp.now()
data = {'time': time,
       'in': np.random.random(1)*1000}
df = pd.DataFrame(data)

# Bulk inserting documents. Each row in the DataFrame will be a document in Mongo
vzlogger.insert_many(df.to_dict('records'))

