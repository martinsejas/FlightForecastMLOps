''' 
This script is to make a fully industralized model. 

We are going to train on the full dataset, and are going to choose a Elastic Net Linear Regressionthe best performing model evaluated on the exploratory notebook called '1.0-MHS-ExploratoryNoteboook'.
Found under model/notebooks
'''


import pandas as pd
import numpy as np
import joblib 
from sklearn.preprocessing import (StandardScaler, OneHotEncoder)
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import PolynomialFeatures

#Reading csv
df = pd.read_csv("model/raw_data/flight-price-training.csv")

#dropping index column
df = df.drop(columns=df.columns[0]) 

#Separating labels from dataset
Y = df['price']

#Dropping unnecessary columns
X = df.drop(columns=['price','flight'])

#making functions for encoding
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


#Starting pre-processing
X = process_stops_column(df=X)

#separating categorical columns and numerical columns
categorical_columns = (X.select_dtypes(include=['object'])).columns
numerical_columns = list(set(X.columns) - set(categorical_columns))

#making encoders
pre_processor_features = ColumnTransformer(
                [("ohe", OneHotEncoder(drop='if_binary', sparse_output=False, handle_unknown='ignore'), categorical_columns),
                 ("std", StandardScaler(), numerical_columns)
                ])
#making encoders
pre_processor_predictions = StandardScaler()

#Reshaping y for encoding
Y = (Y.to_numpy()).reshape(-1,1)


#saving pre-processors
pre_processor_features.fit(X)
joblib.dump(pre_processor_features, "backend/models/pre_processor_features.joblib")

pre_processor_predictions.fit(Y)
joblib.dump(pre_processor_predictions, "backend/models/pre_processor_predictions.joblib")

#Transforming data
X_scaled = pre_processor_features.transform(X)
Y_scaled = pre_processor_predictions.transform(Y)


#creating polynomial transformer
poly = PolynomialFeatures(2)
poly.fit(X_scaled)

#saving polynomial transformer
joblib.dump(poly,"backend/models/feature_transformer.joblib")

#Creating the model
main_model = ElasticNetCV(random_state=42, max_iter=10000)

#Fitting the Model
main_model.fit(X=poly.transform(X_scaled), y = Y_scaled.ravel())

#Saving the model
joblib.dump(main_model,"backend/models/model.joblib")