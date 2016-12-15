import psycopg2
import sys, csv
from glob import glob
#Use pyscopg2 to create connection and then cursor. Will user cursor.execute() to do sql

conn = psycopg2.connect("host='localhost' dbname='ABS' user='postgres' password='password'")
cursor = conn.cursor()

# create pg_routing table on ways 
a = 'ALTER TABLE ways ADD COLUMN "source" integer;'
b = 'ALTER TABLE ways ADD COLUMN "target" integer;'
c = "SELECT pgr_createTopology('ways', 0.00001, 'the_geom', 'gid');"
d = 'CREATE INDEX ways_source_idx ON ways("source");'
e = 'CREATE INDEX ways_target_idx ON ways("target");'



# find nearest point from addresses to road node
# give every address point an attrribute which is closest road point id.

# update srid
'''
ALTER TABLE sa1_2011_aust  
  ALTER COLUMN geom TYPE geometry(multipolygon, 3308) 
    USING ST_SetSRID(geom,3308);
'''
# select centroids
'''
select st_centroid(geom), gid from sa1_2011_aust;
'''

# find closest road ID relative to sa1 7 digit geom, and create concordance
'''
(SELECT  DISTINCT ON(g1.id) g1.the_geom g1.id As sa1_id, g1.sa1_7digit as sa1_7digit, g2.id as road_id2 into table sa1_road_concordance
    FROM (select st_centroid(the_geom) as the_geom, id, sa1_7digit from abs_sa1_2011 ) As g1, ways_vertices_pgr As g2   
    WHERE g1.id <> g2.id AND ST_DWithin(g1.the_geom, g2.the_geom, 6000)   
    ORDER BY g1.id, ST_Distance(g1.the_geom,g2.the_geom));
    alter table sydney_sa1 add column distance_to_closest_park float;
    alter table sydney_sa1 add column closest_park_id int;
'''

# create abs_sydney
'''create table sydney_sa1 as (select distinct abs_sa1_2011.sa1_7digit, abs_sa1_2011.the_geom from abs_sa1_2011, ways where st_intersects(abs_sa1_2011.the_geom, ways.the_geom ))'''

# add closest park column to abs_sydney

closestPark = '''alter table sydney_sa1 add column distance_to_closest_park float;'''


# cull sites touching a park



# for each park get multiple points representing access to road

'''
select parks.gid as park_id, ways_vertices_pgr.id from parks, ways_vertices_pgr 
where st_dwithin(parks.geom, ways_vertices_pgr.the_geom, 50);
'''

# for every park find distance from every park node to every siteNodes 

'''select park_id,id from parkexit_road_concordance, parks where parkexit_road_concordance.park_id = parks.gid ;
'''


# loop through parks and find distance, alter table with min(newDist,oldDist)

'''select sa1_7digit from sydney_sa1;'''

def getOneColumnValues(columnName, tableName):
	'''selects one column from a table'''
	cursor.execute('''select %s from %s;''')
	sydneySa17digit =  cursor.fetchall()
	sydneySa17digit = [x[0] for x in sydneySa17digit]
	return sydneySa17digit

# print sydneySa17digit

for site in sydneySa17digit:
	# site = sydneySa17digit[i]
	cursor.execute('''
	update sydney_sa1 set distance_to_closest_park = result.cost, closest_park_id = result.park_id from 
	(select foo.cost, park_id from (
	       SELECT * FROM pgr_drivingDistance('
	       SELECT gid as id,
	          source,
	          target,
	          shape_leng::float8 AS cost
	       FROM ways'::text,
	       (select road_id from sa1_road_concordance where sa1_7digit::int = %s)::int ,
	       5000,
	       false,
	       false)) as foo,parkexit_road_concordance where foo.id1 = parkexit_road_concordance.id order by cost limit 1) as result where sydney_sa1.sa1_7digit::int = %s;
	''' %(site,site))
	conn.commit()

# for command in sequence:
# 	print command
# 	cursor.execute(command);
# 	conn.commit()

cursor.close()
conn.close()	