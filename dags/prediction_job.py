from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
import pandas as pd
from airflow.exceptions import AirflowSkipException
import os
import requests
import json

DIRECTORY = "/mnt/c/Users/Martin/Documents/FlightPricePrediction/airflow-data/FolderC"


PREDICTIONS_URL = "http://127.0.0.1:8000/predict/" 

HEADERS = {'Content-type': 'application/json'}

default_args = {
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


@task(task_id="check_for_new_data")
def check_for_files(**kwargs):
    raw_line = ""
   
    #making a list to hold the paths of new files
    past_files = []
    files_in_folder = []
    new_files = []
   
    #check previous files
    with open(DIRECTORY+"/filesread.txt", "r") as reading_files:
        for line in reading_files:
            raw_line+=line
   
    past_files = raw_line.split(",")
     #loop through current files
    for filename in os.listdir(DIRECTORY):
        file_path = os.path.join(DIRECTORY,filename)
        files_in_folder.append(file_path)
    
    #make a list of new files
    
    for file in files_in_folder:
        if file not in past_files:
            new_files.append(file)
    
    #writing read files
    with open(DIRECTORY+"/filesread.txt", "w") as writing_files:
           for path in files_in_folder:
               writing_files.write(f"{path},")
               
    if(len(new_files) > 0):
        return new_files
    else:
        raise AirflowSkipException
            
@task(task_id="make_predictions", retries=0)
def make_automatic_predictions( **kwargs):
   ti = kwargs['ti']
   files = ti.xcom_pull(task_ids='check_for_new_data')
   
   print(f"Files are {files}")
   #make a base df out of the first file in the list
   base_df = pd.read_csv(files[0])
   
 
   
   #merge all other files in one df
   for i in range(1,len(files)):
       file_df = pd.read_csv(files[i])
       base_df = pd.concat([base_df,file_df])

   print(f"columns BEFORE CHANGE are: {base_df.columns}")
   base_df = base_df.drop(columns=['price'])
   base_df["class_"] = base_df["class"].copy()
   base_df = base_df.drop(columns=["class"])
  
   base_df = base_df.drop(base_df.columns[0], axis=1)
   base_df = base_df.reset_index(drop=True)
   print(f"columns AFTER CHANGE are: {base_df.columns}")
       
   #Make it into a payload
   #have to drop price
   #and index
   payload_df = json.dumps(base_df.to_dict(orient='records'), ensure_ascii=False)
   payload_dict = json.loads(payload_df)
   
   
   payload = {"data": payload_dict, "source": "Scheduled"}
   
   print(f"Final payload: {payload}")
   
   response = requests.post(PREDICTIONS_URL, json=payload, timeout=5000, headers=HEADERS)
   
   #If everything ok return OK message
   if response.status_code == 200:
       return "Files successfully sent for prediction"
 
   
   #If not return error
   return f"Error: {response.status_code} - {response.reason}"
   
       
  
    
with DAG(
    dag_id = "prediction_job_dag",
    default_args=default_args,
    description="A DAG for checking for files in a folder and making predictions jobs", 
    start_date= datetime(year=2023, month=6, day=9),
    schedule=timedelta(minutes=5), # Every 5 minutes
    catchup=False,
    tags=["prediction"]
) as  dag:
     
    check_for_new_data = check_for_files()
    
    make_predictions = make_automatic_predictions()
    
    # t2 >> t1
    check_for_new_data  >> make_predictions


