import streamlit as st
import datetime


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
prediction_source = st.selectbox('Prediction source', ('Webapp', 'Scheduled Predictions', 'All'))

#Button to get past predictions
past_predictions = st.button("Get Past Predictions :calendar:", type='primary', use_container_width=True)