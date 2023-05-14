import os, sys
from datetime import datetime
from insurance_pred.exception import InsuranceException
from insurance_pred.logger import logging


FILE_NAME = "insurance.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact")
        except Exception as e:
            raise InsuranceException(e, sys)
        

class DataIngestionConfig:
    
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name="INSURANCE"
            self.collection_name="INSURANCE_PROJECT"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir , "data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception  as e:
            raise InsuranceException(e,sys)      

            
# Convert data into dict
    def convert(self):
        try:
            print_data = self.__dict__
            logging.info(f"printing dict data : {print_data}")
            return print_data
        except Exception  as e:
            raise InsuranceException(e,sys)


class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        pass