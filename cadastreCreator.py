import psycopg2
import json

column = "median_mortgage_repay_monthly"

conn = psycopg2.connect("host='localhost' dbname='mediumdensity' user='app_user' password='password'")
cursor = conn.cursor()

cursor.execute("update table syd_cadastre set %s ")

