from dotenv import load_dotenv
import os
import mysql.connector
import ssl
from mysql.connector import errorcode
import pyodbc

load_dotenv()

# Set up the connection string
server = os.getenv("HOST")
database = os.getenv("DATABASE")
username = "ais-epita"
password = os.getenv("PASSWORD")
driver= '{ODBC Driver 18 for SQL Server}'
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
# config = {
#   'host': os.getenv("HOST"),
#   'user':os.getenv("USERNAME"),
#   'password':os.getenv("PASSWORD"),
#   'database':os.getenv("DATABASE"),
#   'port': 1433,
#   'client_flags': [mysql.connector.ClientFlag.SSL],
#   'ssl_ca': 'C:/Users/Martin/Desktop/Class Exercises/AIS S2/DSP/DigiCertGlobalRootG2.crt.pem',
#   'connect_timeout':1000
# }

# try:
#   conn = mysql.connector.connect(**config)
#   print("Connection established")
# except mysql.connector.Error as err:
#   if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#     print("Something is wrong with the user name or password")
#   elif err.errno == errorcode.ER_BAD_DB_ERROR:
#     print("Database does not exist")
#   else:
#     print(err)
# else:
#   cursor = conn.cursor()

print(server)

# Connect to the database
conn = pyodbc.connect(connection_string)

# Execute a SQL query
cursor = conn.cursor()
# Executing Query
cursor.execute('''CREATE TABLE flights(
            id INT PRIMARY KEY, 
            airline VARCHAR(255), 
            flightcode VARCHAR(10)
);''')


cursor.execute('''
               
               ''')

# Commit the transaction
conn.commit()

# Close the database conn
conn.close()
