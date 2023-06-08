from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
from airflow.exceptions import AirflowSkipException
import os
import requests

DIRECTORY = "/mnt/c/Users/Martin/Documents/FlightPricePrediction/airflow-data/FolderC"

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
   return files
    
with DAG(
    dag_id = "prediction_job_dag",
    default_args=default_args,
    description="A DAG for checking for files in a folder and making predictions jobs", 
    start_date= datetime(2021, 1, 1),
    schedule=timedelta(minutes=5), # Every 5 minutes
    catchup=False,
    tags=["prediction"]
) as  dag:
     
    check_for_new_data = check_for_files()
    
    make_predictions = make_automatic_predictions()
    
    # t2 >> t1
    check_for_new_data  >> make_predictions


