import psycopg2
import sys, csv
from glob import glob
import os
import cStringIO

directory = 'X:\\03_Resources\\VAMPIRE\data\\*'

"""takes a dir and adds tables in postgres for every csv file, column 
for every header, taking primary as a string for a common primary key
and uploads their contained data"""
csvNames =  glob(directory)
a = 1
sql_strings = []
primary = 0
for file in csvNames:
	a += 1
	print a
	with open(file, 'r') as f:
		r = csv.reader(f)
		headers = r.next()
		types = r.next()
		f.close()
	# reader = csv.reader(data)
	data = open(file)
	data.readline()
	second = data.readline()
	second = second.split(',')
	print len(second)
	
	for data in second:
		
def parser(data):		
	try:
		data = int(data)
	except:
		data = float(data)
	except:
		data = str(data)
	finally:
		return data