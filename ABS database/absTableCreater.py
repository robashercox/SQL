import psycopg2
import sys, csv
from glob import glob
import os
import cStringIO
#Use pyscopg2 to create connection and then cursor. Will user cursor.execute() to do sql

conn = psycopg2.connect("host='localhost' dbname='southmetrostudy' user='postgres' password='password'")

#Get csv names using glob module to print all files from dir. Remember double backslash for windows!

# csvNames =  glob('D:\\\abs\\census2011\\2011_BCP_SA1_for_NSW_short-header\\2011 Census BCP Statistical Areas Level 1 for NSW\\NSW\\*')
# csvNames =  glob('X:\\data\\abs\\2011 Census BCP Statistical Areas Level 1 for NSW\\NSW\\*')

#for every csv file name open file of that name, read first row
#and second row, get type of second row and use that to create an
#sql create table statement with types
#print ERROR if error

def parser(data):
	mdata = ''		
	try:
		data = float(data)
		mdata = 'float'
	except:
		data = str(data)
		mdata = 'varchar'
	finally:
		return mdata



directory = 'H:\\landuse16\\*'

"""takes a dir and adds tables in postgres for every csv file, column 
for every header, taking primary as a string for a common primary key
and uploads their contained data"""
csvNames =  glob(directory)
print csvNames
cursor = conn.cursor()
a = 1
sql_strings = []
primary = False

for file in csvNames: 
	a += 1
	# print a
	with open(file, 'r') as f:
		r = csv.reader(f)
		headers = r.next()
		types = r.next()
		f.close()
	# reader = csv.reader(data)
	data = open(file)
	data.readline()
	# data.readline()
	tablename = 'a' + os.path.splitext(os.path.basename(file))[0]
	# print tablename
	columns = ','.join('%s %s' %(name, parser(typos)) for name,typos in zip(headers,types))
	print columns
	try:
		sql_string = ("CREATE TABLE %s (%s);" %(tablename, columns))
		# print sql_string
		cursor.execute(sql_string)
		conn.commit()
		print 'yah'
		# print file
		if primary:
			print "primary! -- " + primary
 			cursor.execute("ALTER TABLE %s ADD PRIMARY KEY (%s);" % (tablename, primary))
			conn.commit()
			print "wat"
		cursor.copy_from(data, tablename, ',', null = "0")
		conn.commit()
		print "data uploaded"
	except Exception,e: 
		print str(e)
		conn.rollback()
		cursor.execute("DROP TABLE %s;" % (tablename))
		conn.commit()
		print 'dropped'
	finally:
		print "all done"

# 'X:/data/abs/2011 Census BCP Statistical Areas Level 1 for NSW/NSW/2011Census_B18_NSW_SA1_short.csv'

#in that same loop, after the creation of the table, import the csv data
#with another sql statement

#print ERROR if error

#done.



cursor.close()
conn.close()