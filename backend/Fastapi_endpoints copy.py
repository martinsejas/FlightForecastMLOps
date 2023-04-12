from dotenv import load_dotenv
import os
import pyodbc
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import uvicorn
from datetime import datetime
from typing import List, Dict, Union


load_dotenv()

#Helper function to flatten dict for parsing
def flatten_dict(d):
    result = {}
    for key, value in d.items():
        if isinstance(value, dict):
            flattened = flatten_dict(value)
            result.update({f"{key}.{k}": v for k, v in flattened.items()})
        else:
            result[key] = value[0]  # assuming all values are lists with a single element
    return result

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


# @app.get("/past_predictions/")
# def read_flight(start_date: str = Query(...), end_date: str = Query(...), prediction_source: str = Query(...)):
    
#     start_date = datetime.strptime(start_date, '%Y-%m-%d')
#     end_date = datetime.strptime(end_date, '%Y-%m-%d')
#     print(f"prediction_source is {prediction_source}")
#     cursor = connection.cursor()
#     if(prediction_source != 'All'):
#         cursor.execute("SELECT * FROM flight_predictions WHERE prediction_time >= %s AND prediction_time <= %s AND prediction_source = %s", (start_date, end_date, (prediction_source,)))
#     else:
#          cursor.execute("SELECT * FROM flight_predictions WHERE prediction_time >= %s AND prediction_time <= %s", (start_date, end_date))
#     my_featuress = cursor.fetchall()
#     flights = []
#     for my_features in my_featuress:
#             flight = {"id": my_features[0], "airline": my_features[1], "source_city": my_features[2], "departure_time": my_features[3], "stops": my_features[4],"arrival_time": my_features[5],
#                     "destination_city": my_features[6], "class": my_features[7], "duration": my_features[8], "price": my_features[9], "prediction_source": my_features[10], "prediction_time": my_features[11]}
#             flights.append(flight)

#     cursor.close()
    
#     print(flights)
#     return flights

@app.get("/past_predictions/")
async def read_flight(start_date: str = Query(...), end_date: str = Query(...), prediction_source: str = Query(...)):
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    cursor = connection.cursor()
    
    print(prediction_source)
    if(prediction_source != 'All'):
        
        my_query = "SELECT * FROM flight_predictions WHERE prediction_time >= ? AND prediction_time <= ? AND prediction_source = ?"
        #my_query = "SELECT * FROM flight_predictions WHERE prediction_source = ?"

        #values = (start_date, end_date, prediction_source)
        values = (start_date, end_date,prediction_source)
        cursor.execute(my_query,values)
    else:
        # my_query = f"SELECT * FROM flight_predictions WHERE prediction_time >= {start_date} AND prediction_time <= {end_date}"
        # my_query("SELECT * FROM flight_predictions")
        cursor.execute("SELECT * FROM flight_predictions")
    my_featuress = cursor.fetchall()
    print(my_featuress)
    flights = []
    for my_features in my_featuress:
            flight = {"id": my_features[0], "airline": my_features[1], "source_city": my_features[2], "departure_time": my_features[3], "stops": my_features[4],"arrival_time": my_features[5],
                    "destination_city": my_features[6], "class": my_features[7], "duration": my_features[8], "price": my_features[9], "prediction_source": my_features[10], "prediction_time": my_features[11]}
            flights.append(flight)
            print(my_features)

    cursor.close()
    
    print(flights)
    return flights

# example my_features for insertion
my_features = {"id":1,"airline":"Delta","source_city":"New York","departure_time":"Morning","stops":"one",
               "arrival_time":"Afternoon","destination_city":"Los Angeles","class":"Business","duration":5.5,"price":500,
               "prediction_source":"User","prediction_time":"2023-04-07T11:31:42.100000"}

# the 'predict' endpoint for predictions and feature/prediction storage in the database
@app.post("/predict/")
async def make_predictions(request: Request, received_my_features: List[Dict[str, Union[str, int, float]]]):
    print(received_my_features)
    
    received_my_features_df = pd.DataFrame(received_my_features)
    
    received_my_features_df["prediction_time"] = datetime.now()
    received_my_features_df["price"] = 42
    received_my_features_df["prediction_source"] = "Webapp"
    cursor = connection.cursor()
    received_my_features = received_my_features_df.to_dict(orient='list')
    received_my_features = flatten_dict(received_my_features)
    query = ("INSERT INTO flight_predictions (airline,flight, source_city, departure_time, stops, arrival_time, destination_city, class, duration, days_left, price, prediction_source, prediction_time)"
          "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)")
    values = (received_my_features["airline"], received_my_features["flight"], received_my_features["source_city"], received_my_features["departure_time"], received_my_features["stops"],
               received_my_features["arrival_time"], received_my_features["destination_city"], received_my_features["class_"], received_my_features["duration"], received_my_features["days_left"],
                 received_my_features["price"], received_my_features["prediction_source"], received_my_features["prediction_time"])
    cursor.execute(query, values)
    connection.commit()
    cursor.close()

    # return 42
    
    return received_my_features_df.to_dict()
   
     

if __name__ == "__main__":
    #flights = read_flight()
    #for flight in flights:
    #     print(flight)
    uvicorn.run(app, host="localhost", port=8000)
