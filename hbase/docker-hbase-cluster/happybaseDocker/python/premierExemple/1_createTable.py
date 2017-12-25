import happybase

connection = happybase.Connection('hbasethrift')

table_name = "demotable"
column_family_name = 'cf1'

# [START creating_a_table]
print('Creating the {} table.'.format(table_name))
connection.create_table(
    table_name,
    {
        column_family_name: dict()  # Use default options.
    })
# [END creating_a_table]

connection.close()