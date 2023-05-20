from insurance_pred.logger import logging
from insurance_pred.exception import InsuranceException
import os, sys
from insurance_pred.utils import get_collection_as_df
from insurance_pred.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from insurance_pred.entity import config_entity
from insurance_pred.components.data_ingestion import DataIngestion
from insurance_pred.components.data_validation import DataValidation
from insurance_pred.components.data_transformation import DataTransformation


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
        data_ingestion_artifact=data_ingestion.initiate_dadta_ingestion()
        

        # data validation

        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)

        data_validation_artifact = data_validation.initiate_data_validation()



        #data transformation:
        data_transformation_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_transformation=DataTransformation(data_transformation_config=data_transformation_config,
                                            data_ingestion_artifact=data_ingestion_artifact)
        
        data_transformation_artifact=data_transformation.initiate_data_transformation()


    except Exception as e:
        print(e, sys)
    