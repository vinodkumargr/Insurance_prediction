import pandas as pd
import numpy as np
import os
import sys
from insurance_pred.exception import InsuranceException
from insurance_pred.config import mongo_client
from insurance_pred.logger import logging


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
    
   
    