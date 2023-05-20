from fastapi import FastAPI, Request, Query, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import uvicorn
from datetime import datetime
from typing import List, Dict, Union
from DatabaseConnection import DatabaseConnection




# the 'past_predictions' endpoint for fetching past predictions from the database
app = FastAPI()

#on startup load model and persistent objects

#setting main database object
database = DatabaseConnection()

TABLE_NAME = "flight_predictions"


# format for timestamp
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


#Get past predictions

@app.get("/past_predictions/")
async def read_flight(start_date: str = Query(...), end_date: str = Query(...), prediction_source: str = Query(...)):
    
    #Reformat input parameters
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
     
    #Setting it on the right format
    sql_start_date = datetime.strftime(start_date, TIMESTAMP_FORMAT)
    sql_end_date = datetime.strftime(end_date,TIMESTAMP_FORMAT)
   
    #Setting right prediction source
    if prediction_source == 'All':
        prediction_source = "'Webapp','Scheduled'"
    else:
        prediction_source = f"'{prediction_source}'"
        
        
    my_query = f"SELECT * FROM flight_predictions WHERE prediction_time >= ? AND prediction_time <= ? AND prediction_source IN ({prediction_source})"
    values = (sql_start_date, sql_end_date)
    database.cursor.execute(my_query, values)
 
    rows = database.cursor.fetchall()

    flights = []
    for row in rows:
            flight = {"id": row[0], "airline": row[1], "flight": row[2], "source_city": row[3], "departure_time": row[4], "stops": row[5],"arrival_time": row[6],
                    "destination_city": row[7], "class": row[8], "duration": row[9], "days_left": row[10], "price": row[11], "prediction_source": row[12], "prediction_time": row[13]}
            flights.append(flight)

    return flights

#Setting basemodels for API     
class Flight(BaseModel):
    airline: str
    flight: str
    source_city: str
    departure_time: str
    stops: str
    arrival_time: str
    destination_city: str
    class_: str
    duration: float
    days_left: int

    class Config:
        orm_mode = True

class Flights(BaseModel):
    data: List[Flight]

    class Config:
        orm_mode = True
        

    

    
@app.post("/predict/")
async def make_predictions(received_my_features: Flights):
    
    
    flights_dict = received_my_features.dict()
    flights_data = flights_dict['data']
    received_my_features_df = pd.json_normalize(flights_data)
    

    received_my_features_df["price"] = 42
    received_my_features_df["prediction_source"] = "Webapp"
    received_my_features_df["prediction_time"] = (datetime.now()).strftime(TIMESTAMP_FORMAT)
 
    
    values = received_my_features_df.values.tolist()


    query = ("INSERT INTO flight_predictions (airline,flight, source_city, departure_time, stops, arrival_time, destination_city, class, duration, days_left, price, prediction_source, prediction_time)"
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)")

    database.cursor.executemany(query, values)
    database.connection.commit()
    
    return received_my_features_df.to_dict()
   
     

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
