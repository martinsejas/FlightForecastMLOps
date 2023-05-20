'''
This tests the database connection to the Azure database using a simple SELECT *

This script was authored by Martin Sejas 

'''

from DatabaseConnection import DatabaseConnection

db = DatabaseConnection()


# # Execute a SQL query
# cursor = connection.cursor()
# # Executing Query


# '''
# The db.cursor.commit() method in Pyodbc is used to commit any pending transactions to the database. 
# It is necessary to call this method after executing any INSERT, UPDATE, or DELETE queries 
# to ensure that changes are permanently written to the database. 
# If you don't commit the transaction, the changes will be lost when the connection to the database is closed.
# '''


# # cursor.commit()


db.cursor.execute("SELECT * FROM flight_predictions")


rows = db.cursor.fetchall()

for row in rows:
  print(row)

# # Close the database conn
  
db.close()









