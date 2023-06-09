import pandas as pd
import random
from datetime import datetime

# This script will simply generate 1 or more random csv's on the 'clean' data folder 
# In our case folder C

COLUMNS_CSV = ['airline', 'flight', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class_', 'duration', 'days_left','price']

df = pd.read_csv("data_folders/Airflow_data.csv")
TIMESTAMP_FORMAT = "%Y-%m-%d-%H:%M:%S"

#generate a random number of new files from 1 to 5
number_of_new_files = random.randint(1,5)

#For each new file, select 15-40 random rows, and make a csv
#Write csv to FolderC
for new_file in range(number_of_new_files):
    #Select 15-40 random rows
    number_of_random_rows = random.randint(15,40)
    
    new_df = df.sample(n=number_of_random_rows)
    
    new_df = new_df.iloc[:,1:]
    
    creation_date = datetime.strftime(datetime.now(), TIMESTAMP_FORMAT)

    new_df.to_csv(f"FlightPricePrediction/airflow-data/FolderC/{creation_date}-{new_file+1}.csv")