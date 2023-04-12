'''
This script gets the right database credentials from a .env file located at the root of the repository.
It creates a connection object (cursor) to a dedicated Azure SQL database made for this project.

This script was authored by Martin Sejas 

'''

from dotenv import load_dotenv
import os
import pyodbc

load_dotenv()

# Set up the connection string
server = os.getenv("HOST")
database = os.getenv("DATABASE")
username = os.getenv("DBUSERNAME")
password = os.getenv("PASSWORD")
driver= '{ODBC Driver 18 for SQL Server}'
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Connect to the database
connection = pyodbc.connect(connection_string)



# Execute a SQL query
cursor = connection.cursor()
# Executing Query


'''
The cursor.commit() method in Pyodbc is used to commit any pending transactions to the database. 
It is necessary to call this method after executing any INSERT, UPDATE, or DELETE queries 
to ensure that changes are permanently written to the database. 
If you don't commit the transaction, the changes will be lost when the connection to the database is closed.
'''


# cursor.commit()
cursor.execute("SELECt * FROM flight_predictions")



rows = cursor.fetchall()

for row in rows: 
  print(row)

# Close the database conn
connection.close()
