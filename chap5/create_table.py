import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table1 = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table1)

create_table2 = "CREATE TABLE IF NOT EXISTS bookList (bookID INTEGER PRIMARY KEY, name text, author text)"
cursor.execute(create_table2)

connection.commit()

connection.close()
