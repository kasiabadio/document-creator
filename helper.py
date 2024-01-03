import sqlite3
cursor = None
connection = None

def delete_from_table(table, id):
    global cursor
    global connection
    sql_query = "DELETE FROM " + table + " WHERE id = " + str(id)
    cursor.execute(sql_query)
    connection.commit()

connection = sqlite3.connect("test-gen-db.db")
cursor = connection.cursor()

delete_from_table("subkategoria", 3)
delete_from_table("subkategoria", 2)
delete_from_table("subkategoria", 1)
