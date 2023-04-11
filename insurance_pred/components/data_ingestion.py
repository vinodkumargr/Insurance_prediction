import pandas as pd
import os, sys
import numpy as np
from insurance_pred.entity import config_entity
from insurance_pred.entity import artifacts_entity
from insurance_pred.exception import InsuranceException
from insurance_pred import utils
from insurance_pred.logger import logging
from sklearn.model_selection import train_test_split



class DataIngestion: # data divide into test, train and validate
    def __init__(self, data_ingestion_config: config_entity.DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise InsuranceException(e, sys)
        
        

    def initiate_data_ingestion(self)-> artifacts_entity.DataIngestionArtifact:
        try:
            logging.info(f"export colletion data as pd.DataFrame")
            df:pd.DataFrame = utils.get_collection_as_df(
                database_name= self.data_ingestion_config.database_name,
                collection_name= self.data_ingestion_config.collection_name
            )
            logging.info("save data into feature store")
            
            # replace an with NAN
            df.replace(to_replace = "na", value=np.NAN, inplace=True)
            
            # save data in future store
            logging.info("create feature store folder, if not available")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            
            logging.info("save df to feature store folder")
            
            # save df to feature store
            df.to_csv(path_or_buf = self.data_ingestion_config.feature_store_file_path, index=False, header=True)
            
            logging.info("spliting data into train and test")
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.test_size, random_state=2)
            
            
            logging.info("create dataset_dir if not exist")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok=True)
            
            logging.info("save dataset to feature store after split")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path, index=False, header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path, index=False, header=True)
            
            # prepare artifact folder:
            logging.info("prepare data_ingestion_artifact")
            data_ingestion_artifact = artifacts_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            
            
            
        except Exception as e:
            raise InsuranceException(e, sys)