from insurance_pred.logger import logging
from insurance_pred.exception import InsuranceException
import os, sys
from insurance_pred.utils import get_collection_as_df
from insurance_pred.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from insurance_pred.entity import config_entity
from insurance_pred.components.data_ingestion import DataIngestion


#def test_logger_and_exception():
#    try:
#       logging.info("Starting test_logger_and_exception")
#        result = 3 / 0
#        print(result)
#        logging.info("Ending point of test_logger_and_excpetion")
#    except Exception as e:
#        logging.debug(str(e))
#        raise InsuranceException(e, sys)
    
    
    
if __name__ == "__main__":
    try:
        #start_training_pipeline()
        #test_logger_and_exception()
        
        #get_collection_as_df(database_name = "INSURANCE", collection_name = "INSURANCE_PROJECT")
        training_pipeline_config= config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config= training_pipeline_config)
        print(data_ingestion_config.convert())
        
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        
    except Exception as e:
        print(e, sys)
    