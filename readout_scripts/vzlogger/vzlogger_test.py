import pandas as pd
import subprocess
from pymongo import MongoClient
import numpy as np
import datetime
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
	# capture the relevant output
	print(res)

	# add to dictionary

	# return
	# return res

read_vzlogger('test')