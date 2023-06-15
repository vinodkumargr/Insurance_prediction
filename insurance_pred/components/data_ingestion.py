import pandas as pd
import numpy as np
import os, sys
from insurance_pred import utils
from insurance_pred.exception import InsuranceException
from insurance_pred.logger import logging
from insurance_pred.entity import config_entity, artifacts_entity
from sklearn.model_selection import train_test_split


class DataIngestion:
    
    def __init__(self, data_ingestion_config: config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise InsuranceException(e, sys)
        

    def start_data_ingestion(self)-> artifacts_entity.DataIngestionArtifact:
        try:

            logging.info("Starting data ingestion")

            df = pd.read_csv("/home/vinod/projects/Insurance_prediction/insurance.csv")
            df = df.copy()

            #df=pd.DataFrame = utils.get_as_df(database_name=self.data_ingestion_config.database_name,
            #                                collection_name=self.data_ingestion_config.collection_name)
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            logging.info("got data from mongodb")

            x_train, x_test = train_test_split(df, test_size=0.2)

            logging.info("storing train data")
            x_train.to_csv(path_or_buf = self.data_ingestion_config.train_path, index=False, header=True)
            x_test.to_csv(path_or_buf = self.data_ingestion_config.test_path, index=False, header=True)

            
            #preparing artifacts folder:
            data_ingestion_artifact = artifacts_entity.DataIngestionArtifact(
                train_data_path=self.data_ingestion_config.train_path,
                test_data_path=self.data_ingestion_config.test_path)

            return data_ingestion_artifact

        except Exception as e:
            raise InsuranceException(e,sys)



