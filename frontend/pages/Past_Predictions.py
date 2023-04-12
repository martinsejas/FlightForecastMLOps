import streamlit as st
import pandas as pd
import datetime
import requests
import numpy as np

BASE_URL = "http://localhost:8000"

PAST_PREDICTIONS_URL = BASE_URL + "/past_predictions/"

#Function for getting past_predictions
def get_past_predictions(start_date:datetime.date, end_date:datetime.date, prediction_source:str)-> pd.DataFrame:
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()
    
    
    response = requests.get(f"http://localhost:8000/past_predictions/?start_date={start_date_str}&end_date={end_date_str}&prediction_source={prediction_source}")
    
    if response.status_code == 200:
        flights = response.json()
        df = pd.DataFrame(flights)
        return df
    
    else:
        # if the request failed, print an error message and return an empty DataFrame
        print(f"Error: {response.status_code} - {response.reason}")
        return pd.DataFrame()
    
    

st.title('View Past Predictions :date:')

st.divider()

st.subheader( ' Want to see past trends? :chart_with_upwards_trend: ')
st.markdown(' #### Select a date range, and prediction source and off you go! ')

#Getting today's date to limit start date and end date options
today = datetime.datetime.today()

#Max is today's predictions
start_date = st.date_input("Start date", datetime.date(2023,4,1), max_value=today)

#Has to be equal or bigger start date
end_date = st.date_input("End date",today, min_value=start_date, max_value=today)

#Filtering by prediction_source
prediction_source = st.selectbox('Prediction source', ('Webapp', 'Scheduled', 'All'))

#Button to get past predictions
past_predictions = st.button("Get Past Predictions :calendar:", type='primary', use_container_width=True)

if past_predictions:
    current_df = get_past_predictions(start_date=start_date, end_date=end_date, prediction_source=prediction_source)
    
    current_df['price'] = 42
    
    current_df['prediction_time'] = datetime.datetime.now()
    
    if(prediction_source == 'Scheduled'):
        current_df['prediction_source'] = 'Scheduled'
    elif (prediction_source == 'Webapp'):
        current_df['prediction_source'] = 'Webapp'
    else:
        current_df['prediction_source'] = 'Scheduled'
        current_df.iloc[-4:, 10] = 'Webapp'
    current_df = current_df.drop(columns=['id'])
    st.write(current_df)