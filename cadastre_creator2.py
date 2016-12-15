import psycopg2
import sys, csv
from glob import glob
import os
import cStringIO

conn = psycopg2.connect("host='localhost' dbname='southmetrostudy' user='postgres' password='password'")
cursor = conn.cursor()

tableColDict = {
# 'strata_lt9':'strata_lt9',
# 'strata_gt10':'strata_gt10',
# 'special_use':'special_use',
# 'anef_contours_commercial':'anef_commercial',
# 'anef_contours_constraints':'anef_constraints',
# 'anef_contours_industrial':'anef_industrial',
# 'anef_contours_residential':'anef_residential',
# 'conservation_area':'conservation_area',
# 'env_conservation':'env_conservation',
# 'open_space':'open_space',
'threatened_ecological_communities':'threatened_eco',
'recent_development_98_to_15':'recent_dev'
# 'heritage':'heritage'
}


intersectLayers = tableColDict.keys() 
print intersectLayers

for layer in intersectLayers:
	tablename = layer

	# add col names SQL and then dictMaker
	addcolumn = ('alter table cadastre add column %s int' %(tableColDict[tablename])) 
	try:
		cursor.execute(addcolumn)
		conn.commit()
	except Exception,e:
		print str(e)
		conn.rollback()
		print 'already there'
	finally:
		print 'done'
		

for layer in intersectLayers:
	tablename = layer
	btablename='b_'+tablename


	# create buffered table
	createbuffer = ("create table %s as select a.gid,st_buffer(a.geom,-1) as geom from %s a" %(btablename,tablename))

	# add spatiol index
	addspatialindex = ('CREATE INDEX %s_geom_idx ON %s USING gist (geom);' %(btablename,btablename))

	# add primary key
	addprimarykey = (('alter table %s add primary key (gid)') %(btablename))

	# update cadastre based on tablename
	updatecadastre = ('''update cadastre a set %s = 
	case when st_intersects(a.geom,b.geom) then 1 else 0 end
	from %s b
	where st_intersects(a.geom,b.geom)
	'''%(tableColDict[tablename], btablename))

	# set nulls to 0
	nulltozero = ('update cadastre a set %s = 0 where %s is null;'  %(tableColDict[tablename],tableColDict[tablename]))

	try:
		print tablename + '...'
		try:
			cursor.execute("DROP TABLE %s;" % (btablename))
			conn.commit()
			print 'dropped'
		except Exception,e:
			print str(e)
			conn.rollback()
			print 'not there'
		finally:
			print 'moving on'
		cursor.execute(createbuffer)
		conn.commit()
		print 'buffer created'
		cursor.execute(addspatialindex)
		conn.commit()
		print 'spatial index added'
		cursor.execute(addprimarykey)
		conn.commit()
		print 'primary key added'
		cursor.execute(updatecadastre)
		conn.commit()
		print 'cadastre updated'
	

	except Exception,e:
		print str(e)
		conn.rollback()
		print 'error!'
	

	finally:
		print 'wa wa!'


'''
update cadastre set constraint_code = 
case when open_space then 1
when special_use then 2
when env_conservation then 3
when strata_gt10  = 1then 4
when strata_lt9 = 1 then 5
when recent_dev = 1then 6
when conservation_area = 1  then 7
when heritage = 1 then 8
when flooding = 1 then 9
when te_communities = 1 then 10
when anef_residential = 1 then 11
when anef_commercial =1 then 12
when anef_industrial =1 then 13
'''
# # final SQL loop to get attributes of zoning

# addfsrcol = 'alter table cadastre add column fsr float;'
# addlzncol = 'alter table cadastre add column lzn varchar(10);'

# updatefsr = '''update cadastre set fsr = b.fsr
# from fsr b
# where st_within(st_centroid(cadastre.geom),b.geom)'''

# updatelzn = '''update cadastre set lzn = b.sym_code
# from lzn b
# where st_within(st_centroid(cadastre.geom),b.geom)'''

# try:
# 	cursor.execute(addfsrcol)
# 	conn.commit()
# 	print 'fsr col added'
# 	cursor.execute(addlzncol)
# 	conn.commit()
# 	print 'lzn col added'
# 	cursor.execute(updatefsr)
# 	conn.commit()
# 	print 'fsr added'
# 	cursor.execute(updatelzn)
# 	conn.commit()
# 	print 'lzn added'
# except Exception,e:
# 	print str(e)
# 	conn.rollback()
# 	print 'error'


cursor.close()
conn.close()