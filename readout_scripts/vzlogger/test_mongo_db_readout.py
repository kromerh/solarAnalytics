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


# ====== Finding Documents ====== #
documents = vzlogger.find()
df = pd.DataFrame(list(documents))
print(df)