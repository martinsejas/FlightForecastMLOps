"""
    This class 'DatabaseConnection' encapusaltes the pyodbc 'connection' and 'cursor' object, 
    it also allows us to use a single object for the database connection.
"""

import os
import pyodbc


class DatabaseConnection:
    def __init__(self) -> None:
        server = "dsp-group3.database.windows.net"
        database = "flight-prediction"
        username = "ais-epita"
        password = "DSPgroup3*"
        driver= '{ODBC Driver 18 for SQL Server}'
        self.connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()
        
    def close(self) -> None:
        self.connection.close()
        


    