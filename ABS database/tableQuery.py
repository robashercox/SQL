import psycopg2
import itertools 

conn = psycopg2.connect("host='localhost' dbname='ABS' user='postgres' password='password'")

cursor = conn.cursor()

def census2011Padder(table):
	"""adds padding to table number"""
	return "a2011census_%s_nsw_sa1_short" %table

b46 = census2011Padder('b46')

def selectAll(table):
	"""select all columns from a table"""
	cursor.execute("Select * from %s" %(table))
	rows = cursor.fetchall()
	colnames = [desc[0] for desc in cursor.description]
	return [colnames,rows]

b46names = selectAll(b46)[0]
b46data = selectAll(b46)[1]

b46namesFilterMask = [1 if ((('trn' in name) or ('train' in name)) and ('_p' in name)) else 0 for name in b46names]
runningTotal = [0 for name in b46names if ((('trn' in name) or ('train' in name)) and ('_p' in name))] 
a = 0
results = []
for row in b46data:
	a += 1
	filteredRow = itertools.compress(row, b46namesFilterMask)
	total = sum(filteredRow)
	id = row[0]
	results.append([id,total])

print results[0]

def createColumn(table, columnName, columnType):
	"""create column of columnType in table"""
	cursor.execute("Select * from %s LIMIT 0" %(table))
	colnames = [desc[0] for desc in cursor.description]
	if columnName not in colnames:
		cursor.execute("Alter table %s add column %s %s" %(table, columnName,columnType))
		conn.commit()

def insertValue(table, columnName, value, idcolunmName, id):
	"""insert a value into a column where id = value"""
	cursor.execute("Select * from %s LIMIT 0" %(table))
	colnames = [desc[0] for desc in cursor.description]
	if columnName in colnames:
		cursor.execute("Update %s set %s = %s where %s = %s" %(table, columnName, value,idcolunmName,id))
		conn.commit()

for result in results:
	insertValue(b46,"total_using_train",result[1],"region_id",result[0])

# createColumn(b46, "total_using_train", "float"):





