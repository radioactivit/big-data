import happybase

connection = happybase.Connection('hbasethrift')

table_name = "demotable"
column_family_name = 'cf1'

# [START deleting_a_table]
print('Deleting the {} table.'.format(table_name))
connection.delete_table(table_name,1)
# [END deleting_a_table]


connection.close()
