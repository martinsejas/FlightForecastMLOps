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
        sql_start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        sql_end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        values = (sql_start_date, sql_end_date,prediction_source)
        print(values)
        cursor.execute(my_query,values)
    else:
        # my_query = f"SELECT * FROM flight_predictions WHERE prediction_time >= {start_date} AND prediction_time <= {end_date}"
        sql_start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        sql_end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        my_query = "SELECT * FROM flight_predictions  WHERE prediction_time >= ? AND prediction_time <= ?"
        values = (sql_start_date, sql_end_date)
        cursor.execute(my_query, values)
    my_featuress = cursor.fetchall()
    # print(my_featuress)
    flights = []
    for my_features in my_featuress:
            flight = {"id": my_features[0], "airline": my_features[1], "flight": my_features[2], "source_city": my_features[3], "departure_time": my_features[4], "stops": my_features[5],"arrival_time": my_features[6],
                    "destination_city": my_features[7], "class": my_features[8], "duration": my_features[9], "days_left": my_features[10], "price": my_features[11], "prediction_source": my_features[12], "prediction_time": my_features[13]}
            flights.append(flight)
            #print(my_features)

    cursor.close()
    
    #print(flights)
    return flights


    
    
    
@app.post("/predict/")
async def make_predictions(request: Request, received_my_features: List[Dict[str, Union[str, int, float]]]):
    print(received_my_features)

    received_my_features_df = pd.DataFrame(received_my_features)

    cursor = connection.cursor()

    for index, row in received_my_features_df.iterrows():
        received_my_features = row.to_dict()
        received_my_features["prediction_time"] = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        received_my_features["price"] = 42
        received_my_features["prediction_source"] = "Webapp"
        print(received_my_features)

        # received_my_features = flatten_dict(received_my_features)
        query = ("INSERT INTO flight_predictions (airline,flight, source_city, departure_time, stops, arrival_time, destination_city, class, duration, days_left, price, prediction_source, prediction_time)"
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)")
        values = (received_my_features["airline"], received_my_features["flight"], received_my_features["source_city"], received_my_features["departure_time"], received_my_features["stops"],
                   received_my_features["arrival_time"], received_my_features["destination_city"], received_my_features["class_"], received_my_features["duration"], received_my_features["days_left"],
                     received_my_features["price"], received_my_features["prediction_source"], received_my_features['prediction_time'])
        cursor.execute(query, values)
        connection.commit()

    cursor.close()

    
    return received_my_features_df.to_dict()
   
     

if __name__ == "__main__":
    #flights = read_flight()
    #for flight in flights:
    #     print(flight)
    uvicorn.run(app, host="localhost", port=8000)
