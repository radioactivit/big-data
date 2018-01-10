import happybase

connection = happybase.Connection('hbasethrift')

table_name = "demotable"
column_family_name = 'cf1'

# [START writing_rows]
print('Writing some greetings to the table.')
table = connection.table(table_name)
column_name = '{fam}:greeting'.format(fam=column_family_name)
greetings = [
    'Hello World!',
    'Hello Cloud Bigtable!',
    'Hello HappyBase!',
]

for i, value in enumerate(greetings):
    # Note: This example uses sequential numeric IDs for simplicity,
    # but this can result in poor performance in a production
    # application.  Since rows are stored in sorted order by key,
    # sequential keys can result in poor distribution of operations
    # across nodes.
    #
    # For more information about how to design a Bigtable schema for
    # the best performance, see the documentation:
    #
    #     https://cloud.google.com/bigtable/docs/schema-design
    row_key = 'greeting{}'.format(i)
    table.put(row_key, {column_name: value})
# [END writing_rows]

connection.close()
