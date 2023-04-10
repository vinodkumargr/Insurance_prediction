import pandas as pd
import numpy as np
import os
import sys
from insurance_pred.exception import InsuranceException
from insurance_pred.config import mongo_client
from insurance_pred.logger import logging


def get_collection_as_df(database_name:str, collection_name:str):
    try:
        logging.info(f"Reading data from database :{database_name} and collection name : {collection_name}")
        df = pd.DataFrame(mongo_client[database_name][collection_name].find())
        logging.info(f"Total columns found : {df.columns}")
        if "index" in df.columns:
            logging.info("Dropping columns: Index")
            df = df.drop("index", axis=1)
        logging.info(f"Dataframe shape : {df.shape}")
        return df
    
    except Exception as e:
        raise InsuranceException(e, sys)
    