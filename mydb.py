from mysql.connector import connect

# Connect to the database
dataBase = connect(
		host = 'localhost',
		user = 'root',
		passwd = 'tingi'
	)

# Create cursor object
cursorObject = dataBase.cursor()

# Create database
cursorObject.execute("CREATE DATABASE crm_backend");

print("Database created!")