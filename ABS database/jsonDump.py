import psycopg2
import sys, csv
from glob import glob
import os
import cStringIO
import json
#Use pyscopg2 to create connection and then cursor. Will user cursor.execute() to do sql

conn = psycopg2.connect("host='localhost' dbname='ABS' user='postgres' password='password'")


# print csvNames
cursor = conn.cursor()
cursor.execute("SELECT JSON_AGG(T) FROM AVAMPIRE AS T")
bigJson = json.dumps(cursor.fetchall()[0]).encode('utf8')
print bigJson


cursor.close()
conn.close()


