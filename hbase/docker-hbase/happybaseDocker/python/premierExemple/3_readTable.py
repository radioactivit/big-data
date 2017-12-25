import happybase

connection = happybase.Connection('hbasethrift')

table_name = "demotable"
column_family_name = 'cf1'
column_name = '{fam}:greeting'.format(fam=column_family_name)

table = connection.table(table_name)

# [START getting_a_row]
print('Getting a single greeting by row key.')
key = 'greeting0'.encode('utf-8')
row = table.row(key)
print('\t{}: {}'.format(key, row[column_name.encode('utf-8')]))
# [END getting_a_row]

# [START scanning_all_rows]
print('Scanning for all greetings:')

for key, row in table.scan():
    print('\t{}: {}'.format(key, row[column_name.encode('utf-8')]))
# [END scanning_all_rows]

connection.close()