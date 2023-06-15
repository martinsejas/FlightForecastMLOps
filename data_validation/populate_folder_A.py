import pandas as pd
import os
import random


def alter_rows(df):
    num_rows = len(df)
    num_altered_rows = int(0.2 * num_rows)  # 20% of rows to be altered

    altered_rows = random.sample(range(num_rows), num_altered_rows)

    for row in altered_rows:
        # Randomly select a subset of columns to alter
        num_columns = len(df.columns)
        columns_to_alter = random.sample(range(num_columns), random.randint(1, num_columns))

        # Set the values of the selected columns in the row to NaN
        df.iloc[row, columns_to_alter] = pd.NA

    return df


def malformat_data(df):
    df[:] = pd.NA  # Set all values to NaN
    return df


def split_dataframe(df, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Calculate the number of rows per file
    rows_per_file = len(df) // 1000

    # Split the DataFrame into multiple smaller DataFrames
    dfs = [df[i:i+rows_per_file] for i in range(0, len(df), rows_per_file)]

    # Save each DataFrame as a separate CSV file
    for i, df_split in enumerate(dfs):
        filename = os.path.join(output_folder, f"file_{i}.csv")
        
        probability = random.random()
        
        if probability <= 0.7:
            #continue as normal 70%
            filename = os.path.join(output_folder, f"file_{i}_GOOD.csv")
            df_split.to_csv(filename, index=False)
            
        elif probability > 0.7 and probability <= 0.9:
            # modify some 20%
            filename = os.path.join(output_folder, f"file_{i}_CHANGED.csv")
            altered_df = alter_rows(df_split.copy())
            altered_df.to_csv(filename, index=False)
        
        else: 
            #malformat everything 10%
            filename = os.path.join(output_folder, f"file_{i}_BAD.csv")
            malformatted_df = malformat_data(df_split.copy())
            malformatted_df.to_csv(filename, index=False)


# Load the DataFrame from a CSV file
csv_file = "/mnt/c/Users/Martin/Documents/data_folders/Airflow_data.csv"
df = pd.read_csv(csv_file)

# Split the DataFrame into 1000 CSV files with different options
output_folder = "/mnt/c/Users/Martin/Documents/data_folders/FolderA"

#calling the function

split_dataframe(df=df,output_folder=output_folder)



