import numpy as np
import pandas as pd
import joblib

FOLDER_PATH = "backend/persisted_models/"

def encode_stops(s:str)-> int:
    if (s == 'one'):
        return 1
    elif(s == 'zero'):
        return 0
    else:
        return 2
    
def process_stops_column(df: pd.DataFrame)->pd.DataFrame:
    df['stops'] = df['stops'].apply(encode_stops)
    return df





def get_predictions(df: pd.DataFrame)-> np.array:
    # need to pre_process data, 
    # then pass through feature transformer
    # Predict thru model
    # Get inverse predictions
    
    df = process_stops_column(df=df)
    
    #drop unnecessary columns
    df = df.drop(columns=['flight'])
    
    # pre_processing raw data
    pre_processor = joblib.load(filename=FOLDER_PATH+"pre_processor_features.joblib")
    processed_data = pre_processor.transform(df)
    
    #Applying polynomial transformation
    feature_transformer = joblib.load(filename=FOLDER_PATH+"feature_transformer.joblib")
    transformed_data = feature_transformer.transform(processed_data)
    
    #Apply to model now
    model = joblib.load(filename=FOLDER_PATH+"model.joblib")
    scaled_predictions = model.predict(transformed_data)
    
    #Load inverse transformer
    prediction_processor = joblib.load(filename=FOLDER_PATH+"pre_processor_predictions.joblib")
    predictions = prediction_processor.inverse_transform(scaled_predictions.reshape(-1,1))
    
    return predictions
    
    




    
   

