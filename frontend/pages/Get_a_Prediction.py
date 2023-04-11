import streamlit as st

st.title("  Predict the price of your next trip! ")

st.subheader(" Fill in the following information, and we will estimate the price of your trip!	:airplane_departure:")


airline = st.selectbox('What Airline do you want to fly with?', 
                       ('Air India', 'GO FIRST', 'Indigo', 'Vistara', 'AirAsia', 'SpiceJet'))

if(airline == 'Air India'):
    airline = 'Air_India'
    
if(airline == 'GO FIRST'):
    airline = 'GO_FIRST'

source_city = st.radio('What is your origin city?',
                       ('Bangalore', 'Hyderabad', 'Kolkata', 'Mumbai', 'Delhi', 'Chennai'))

departure_time = st.selectbox('What time are you planning to depart?', 
                       ('Early Morning', 'Morning', 'Afternoon', 'Night', 'Late Night'))

if(departure_time == 'Early Morning'):
    departure_time = 'Early_Morning'
    
if(departure_time == 'Late Night'):
    departure_time = 'Late_Night'

stops = st.select_slider(' How many connections are you making?',
                         ('0', '1', '2+'))

if(stops == '0'):
    stops = 'zero'
elif(stops == '1'):
    stops = 'one'
else:
    stops = 'two_or_more'


arrival_time = st.selectbox('What time are you planning to arrive?', 
                       ('Early Morning', 'Morning', 'Afternoon', 'Night', 'Late Night'))

if(arrival_time == 'Early Morning'):
    arrival_time = 'Early_Morning'
    
if(arrival_time == 'Late Night'):
    arrival_time = 'Late_Night'

destination_city = st.radio('Where are you flying to?',
                       ('Bangalore', 'Hyderabad', 'Kolkata', 'Mumbai', 'Delhi', 'Chennai'), key='arrival')

fare_class = st.radio('What class is your ticket?',
                      ('Economy', 'Business'))

duration = st.number_input('What is the total duration of your flight(s)? (hours)',
                           min_value=0.5, max_value=50.0)

days_left = st.number_input('How many days left until your trip?',
                            min_value=1, max_value=49)

if st.button(':ship: Get Prediction! :ship:', type='primary', use_container_width=True):
    st.write('Predicted Flight Price: 42')

