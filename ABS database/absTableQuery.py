import psycopg2
import sys, csv
from glob import glob
import os
import cStringIO
import json
#Use pyscopg2 to create connection and then cursor. Will user cursor.execute() to do sql

conn = psycopg2.connect("host='localhost' dbname='ABS' user='postgres' password='password'")


# SELECT array_to_json(array_agg(t)) FROM t to get json



# print csvNames
cursor = conn.cursor()
cursor.execute("Select * FROM abs_sa1_2011")
colnames = [desc[0] for desc in cursor.description]
medianDict = {}
for name in colnames:
	if 'geom' in name:
		break
	else:
		cursor.execute("""with ordered as (select %s::int, row_number() over (order by %s) as row_id,
		(Select count(1) from abs_sa1_2011) as ct
		from abs_sa1_2011 order by row_id )
		select avg(%s)::int as median from ordered where row_id between ct/2.0 and ct/2.0+1""" %(name,name,name))
		medianDict[name] = int(cursor.fetchall()[0][0])

print medianDict
'''
# fetchall receives a list of tuples, json_agg is also a tuple
bigJson = cursor.fetchall()[0][0]
# set up object
jsons={}
# set up container
jsons['destination'] = bigJson
# remove u' strings
jsonsJson = json.dumps(jsons)

# print jsons
with open("H:\\robashercox.github.io\\data\\jtw.json",'w') as f:
	f.write(str(jsonsJson))
'''



# 'X:/data/abs/2011 Census BCP Statistical Areas Level 1 for NSW/NSW/2011Census_B18_NSW_SA1_short.csv'


#in that same loop, after the creation of the table, import the csv data
#with another sql statement

#print ERROR if error

#done.

cursor.close()
cursor.close()
conn.close()


