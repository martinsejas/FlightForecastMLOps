import streamlit as st
import requests
import pandas as pd
import numpy as np
import json


COLUMNS = ['airline', 'flight', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class_', 'duration', 'days_left']
COLUMNS_csv = ['airline', 'flight', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class_', 'duration', 'days_left','price']
PRINTING_COLUMNS = ['price','airline', 'flight', 'source_city', 'departure_time', 'stops', 'arrival_time',
                    'destination_city', 'class_', 'duration', 'days_left','prediction_source', 'prediction_time']
BASE_URL = "http://localhost:8000"

PREDICTIONS_URL = BASE_URL + "/predict/"

HEADERS = {'Content-type': 'application/json'}

def send_prediction_request(features: pd.DataFrame)-> pd.DataFrame:
    #converting to dictionary
    payload = features.to_dict(orient='records')
    print(payload)
    
    payload= { "data": payload}
    
    print(json.dumps(payload))
   
    
    #Sending as a post request
    response = requests.post(PREDICTIONS_URL, json=payload, timeout=5000, headers=HEADERS)
    
    if response.status_code == 200:
       #decoding (bytes) response with json.loads
        df_content= json.loads(response.content)
        
        response_df = pd.DataFrame(df_content)
        
        return response_df
    else:
        # if the request failed, print an error message and return None
        print(f"Error: {response.status_code} - {response.reason}")
        return None
    
#------------------------------MAIN STREAMLIT APP-------------------------------------------------------------------------------
st.title("  Predict the price of your next trip! ")
st.subheader(" Fill in the following information, and we will estimate the price of your trip!	:airplane_departure:")

#Setting form for feature collection
airline = st.selectbox('What Airline are you flying with?', 
                       ('Air India', 'GO FIRST', 'Indigo', 'Vistara', 'AirAsia', 'SpiceJet'))

#Resetting values for back end purposes
if(airline == 'Air India'):
    airline = 'Air_India'
    
if(airline == 'GO FIRST'):
    airline = 'GO_FIRST'
    
flight_code = st.text_input(label='Flight Number (if not known leave default)', value='AA-0000', max_chars=7)

source_city = st.radio('What is your origin city?',
                       ('Bangalore', 'Hyderabad', 'Kolkata', 'Mumbai', 'Delhi', 'Chennai'))

departure_time = st.selectbox('What time are you planning to depart?', 
                       ('Early Morning', 'Morning', 'Afternoon', 'Night', 'Late Night'))

#Resetting values for back end purposes
if(departure_time == 'Early Morning'):
    departure_time = 'Early_Morning'
    
if(departure_time == 'Late Night'):
    departure_time = 'Late_Night'

stops = st.select_slider(' How many connections are you making?',
                         ('0', '1', '2+'))
#Resetting for back end
if(stops == '0'):
    stops = 'zero'
elif(stops == '1'):
    stops = 'one'
else:
    stops = 'two_or_more'


arrival_time = st.selectbox('What time are you planning to arrive?', 
                       ('Early Morning', 'Morning', 'Afternoon', 'Night', 'Late Night'))

#Resetting for back end
if(arrival_time == 'Early Morning'):
    arrival_time = 'Early_Morning'
    
if(arrival_time == 'Late Night'):
    arrival_time = 'Late_Night'

destination_city = st.radio('Where are you flying to?',
                       ('Bangalore', 'Hyderabad', 'Kolkata', 'Mumbai', 'Delhi', 'Chennai'), key='arrival')

fare_class = st.radio('What class is your ticket?',
                      ('Economy', 'Business'))

#Max values are from dataset
duration = st.number_input('What is the total duration of your flight(s)? (hours)',
                           min_value=0.5, max_value=50.0)

days_left = st.number_input('How many days left until your trip?',
                            min_value=1, max_value=260)

if st.button(':ship: Get Prediction! :ship:', type='primary', use_container_width=True):
        data = [airline,flight_code, source_city, departure_time, stops, arrival_time, destination_city, fare_class, duration, days_left]
        
        data_numpy = np.array(data)
        data_numpy = data_numpy.reshape(1,-1)
        prediction_df = pd.DataFrame(data=data_numpy, columns=COLUMNS)
        actual_prediction = send_prediction_request(prediction_df)
        actual_prediction = actual_prediction[PRINTING_COLUMNS]
        st.write(f"Your prediction is: {(actual_prediction['price'].values[0]):.2f} rupees")
        st.write(actual_prediction.iloc[:, 0:])
        
    

st.divider()
st.subheader("You can also upload a csv file to get many predictions!:parachute:")

st.caption("Note: we only accept csv files with feature values in the right order")


#Accept csv's only
feature_csv = st.file_uploader("Upload Feature CSV", type=["csv"])


#Adding some logic where they can't request predictions without the file being uploaded
predict_many = st.button("Get Predictions :earth_americas:", type='primary', use_container_width=True, disabled=not feature_csv)

if feature_csv and predict_many:

    
    df = pd.read_csv(feature_csv, names=COLUMNS_csv, header=None)
    df = df.drop(columns=['price'])
    predictions = send_prediction_request(df)
    predictions = predictions[PRINTING_COLUMNS]
    st.write(predictions.to_csv(index=False))
    
else:
    st.caption("Please upload file before requesting predictions.")
    
    
    
    
#TODO: fix display of predictions