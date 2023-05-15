#missing values
#otliers handling
#handling imbalance data
#encoding cat to num

from insurance_pred.entity import config_entity, artifacts_entity
from insurance_pred.logger import logging
from insurance_pred.exception import InsuranceException
from insurance_pred import utils
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer 
from sklearn.preprocessing import RobustScaler
from insurance_pred.config import TARGET_COLUMN
from sklearn.preprocessing import LabelEncoder
# if you have imbalance dataset, you use this SMOTE
# from sklearn.combine import SMOTE
import os, sys
import numpy as np
import pandas as pd



class DataTransformation:

    def __init__(self, data_transformation_config:config_entity.DataTransformationConfig, 
                data_ingestion_artifact:artifacts_entity.DataIngestionArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact=data_ingestion_artifact

        except Exception as e:
            raise InsuranceException(e,sys)




    @classmethod
    def get_data_transformer_object(cls)-> Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy='constant', fill_value=0)
            robust_scaler =  RobustScaler()

            pipeline = Pipeline(steps=[
                    ('Imputer',simple_imputer),
                    ('RobustScaler',robust_scaler)
                ])
            
            return pipeline
        
        except Exception as e:
            raise InsuranceException(e, sys)


    def initiate_data_transformation(self,) -> artifacts_entity.DataTransformationArtifact:
        try:
            train_df = pd.read_csv("/home/vinod/projects/Insurance_prediction/artifact/data_ingestion/dataset/train.csv")
            test_df = pd.read_csv("/home/vinod/projects/Insurance_prediction/artifact/data_ingestion/dataset/test.csv")
            
            input_feature_train_df=train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df=test_df.drop(TARGET_COLUMN,axis=1)

            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            label_encoder = LabelEncoder()

            target_feature_train_arr = target_feature_train_df.squeeze()
            target_feature_test_arr = target_feature_test_df.squeeze()

            for col in input_feature_train_df.columns:
                if input_feature_test_df[col].dtypes == 'O':
                    input_feature_train_df[col] = label_encoder.fit_transform(input_feature_train_df[col])
                    input_feature_test_df[col] = label_encoder.fit_transform(input_feature_test_df[col])
                else:
                    input_feature_train_df[col] = input_feature_train_df[col]
                    input_feature_test_df[col] = input_feature_test_df[col]

            transformation_pipleine = DataTransformation.get_data_transformer_object()
            transformation_pipleine.fit(input_feature_train_df)

            input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)
            
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr ]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]


            utils.save_numpy_array_data(file_path=self.data_transformation_config.transform_train_path,
                                        array=train_arr)

            utils.save_numpy_array_data(file_path=self.data_transformation_config.transform_test_path,
                                        array=test_arr)           


            
            utils.save_object(file_path=self.data_transformation_config.transform_object_path,
                            obj=transformation_pipleine)

            utils.save_object(file_path=self.data_transformation_config.target_encoder_path,
                            obj=label_encoder)



            data_transformation_artifact = artifacts_entity.DataTransformationArtifact(
                transform_object_path=self.data_transformation_config.transform_object_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path

            )

            return data_transformation_artifact
        except Exception as e:
            raise InsuranceException(e, sys)