'''
This script gets the right database credentials from a .env file located at the root of the repository, and creates a connection object (cursor).

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
# cursor.execute('''CREATE TABLE flights(
#             id INT PRIMARY KEY, 
#             airline VARCHAR(255), 
#             flightcode VARCHAR(10)
# );''')


cursor.execute('''
                  SELECT * FROM flights         
               ''')

rows = cursor.fetchall()

for row in rows: 
  print(row)

# Close the database conn
connection.close()
