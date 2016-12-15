import psycopg2
import json

column = "median_mortgage_repay_monthly"

conn = psycopg2.connect("host='localhost' dbname='ABS' user='app_user' password='password'")
cursor = conn.cursor()

cursor.execute("select json_agg(t) from (select a.region_id::int, a.median_age::int, a.median_age::int, a.median_mor::int, a.median_ren::int, round(average_nu,1), round(average_ho,1), st_astext(st_transform(a.the_geom,4326)) from abs_sa1_2011 as a join(select * from sydney_sa1 where st_area(the_geom)<900000) as b on a.region_id::int = b.sa1_7digit::int) as t;")

bigJson = json.dumps(cursor.fetchall()[0]).encode('utf')
print bigJson