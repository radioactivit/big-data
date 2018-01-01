import happybase

connection = happybase.Connection('hbasethrift')

table_name = "arbre_paris"

print('Deleting the {} table.'.format(table_name))
connection.delete_table(table_name,1)


connection.close()
