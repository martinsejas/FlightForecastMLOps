from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import requests

#Task to check for new data
def check_for_new_data():
    """n this task, you will check in the folder where the data is ingested if there are any new files (one or multiple). 
    If so read it and pass it to the next task, otherwise mark the dag run status as skipped.
    """
    
def make_predictions():
    """
    in this task, you will make API call to the model service to make predictions on the data read by the previous task.
    
    """

# Sensor to detect a new file in a local folder 

file_sensor = FileSensor(task_id="wait for prediction files", )