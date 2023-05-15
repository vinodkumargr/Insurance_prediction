import pandas as pd
import numpy as np
import os
import sys
from insurance_pred.exception import InsuranceException
from insurance_pred.config import mongo_client
from insurance_pred.logger import logging
import yaml


def get_collection_as_df(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found total columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id")
            df = df.drop("_id",axis=1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df
    
    except Exception as e:
        raise InsuranceException(e, sys)
    


def write_into_yaml(file_path, data: dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, 'w') as write_file:  # Corrected line
            yaml.dump(data, write_file)
    except Exception as e:
        raise InsuranceException(e, sys)



def convert_columns_into_float(df:pd.DataFrame, exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                if df[column].dtype !='O':
                    df[column] = df[column].astype('float')

        return df
    except Exception as e:
        raise InsuranceException(e, sys)



