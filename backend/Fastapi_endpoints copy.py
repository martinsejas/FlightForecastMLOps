from dotenv import load_dotenv
import os
import pyodbc
from fastapi import FastAPI
import uvicorn
import datetime

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




# the 'past_predictions' endpoint for fetching past predictions from the database
app = FastAPI()

#on startup load model and persistent objects


@app.get("/past_predictions/")
def read_flight():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flight_predictions")
    my_featuress = cursor.fetchall()
    flights = []
    for my_features in my_featuress:
            flight = {"id": my_features[0], "airline": my_features[1], "source_city": my_features[2], "departure_time": my_features[3], "stops": my_features[4],"arrival_time": my_features[5],
                    "destination_city": my_features[6], "class": my_features[7], "duration": my_features[8], "price": my_features[9], "prediction_source": my_features[10], "prediction_time": my_features[11]}
            flights.append(flight)

    cursor.close()
    return flights

# example my_features for insertion
my_features = {"id":1,"airline":"Delta","source_city":"New York","departure_time":"Morning","stops":"one",
               "arrival_time":"Afternoon","destination_city":"Los Angeles","class":"Business","duration":5.5,"price":500,
               "prediction_source":"User","prediction_time":"2023-04-07T11:31:42.100000"}

# the 'predict' endpoint for predictions and feature/prediction storage in the database
@app.get("/predict/")
def make_predictions(my_features):
    cursor = connection.cursor()
    my_features["prediction_time"] = datetime.datetime.now()
    query = ("INSERT INTO flight_predictions (airline, source_city, departure_time, stops, arrival_time, destination_city, class, duration, price, prediction_source, prediction_time)"
          "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
    values = (my_features["airline"], my_features["source_city"], my_features["departure_time"], my_features["stops"],
               my_features["arrival_time"], my_features["destination_city"], my_features["class"], my_features["duration"],
                 my_features["price"], my_features["prediction_source"], my_features["prediction_time"])
    cursor.execute(query, values)
    connection.commit()
    cursor.close()

    return 42
     

if __name__ == "__main__":
    #flights = read_flight()
    #for flight in flights:
    #     print(flight)
    uvicorn.run(app, host="localhost", port=8000)
