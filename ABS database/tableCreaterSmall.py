headers = ['fsr_e', 'fsr_p','height_e','height_p','split_e','split_p', 'zoning_e', 'zoning_p', 'dist_trans', 'dist_open', 'a','b', 'c', 'constraint_', 'lga', 'gfa_e','gfa_p']
types = ['float','float','float','float','text','text','text','text', 'float', 'float', 'text','text','text','text', 'text','float','float' ]

columns = ','.join('add column ' + '%s %s' %(name, typos) for name,typos in zip(headers,types))

print len(headers)
print len(types)
print columns
string = []

for header in columns:
	string.append('add column ' + header)

# print string

# 	try:
# 		sql_string = ("CREATE TABLE %s (%s);" %(tablename, columns))