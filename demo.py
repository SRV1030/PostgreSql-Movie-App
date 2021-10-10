import psycopg2

url = "postgres://kzloauih:Crxn49PvFsw1hxxqseb9TBm2twiKlhnL@chunee.db.elephantsql.com/kzloauih"
connection = psycopg2.connect(url)

cursor = connection.cursor()
cursor.execute("SELECT * FROM users")
print(cursor.fetchone())
connection.close()