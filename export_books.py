import sqlite3

conn = sqlite3.connect(database='flask_collection/site.db')

cursor = conn.execute("SELECT * from BOOK")
for row in cursor:
    # TODO: export row information
    print(row)

conn.close()
