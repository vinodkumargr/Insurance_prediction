from insurance_pred.entity import artifacts_entity, config_entity
from insurance_pred.logger import logging
from insurance_pred.exception import InsuranceException

class DataValidation:

    def __init__(self, data_validation_config:config_entity.DataValidationConfig,
                        data_ingestion_artifact:artifacts_entity.DataIngestionArtifact):

        try:
            logging(f"----------------Data Validation process----------------")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise InsuranceException(e, sys)

    def drop_missing_values(self, df:pd.DataFrame)-> [pd.DataFrame]:
        try:

            self.threshold = config_entity.missing_threshold
            self.null_report = df.isnull().sum() / df.shape[0]
            self.drop_column_names = null_report[null_report > threshold]

        except Exception as e:
            raise InsuranceException(e,sys)