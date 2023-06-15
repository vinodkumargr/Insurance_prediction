from insurance_pred.exception import InsuranceException
from insurance_pred.logger import logging
from insurance_pred import config, utils
from insurance_pred.entity import config_entity, artifacts_entity
import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor




class ModelTrainer:

    def __init__(self, model_trainer_config:config_entity.ModeTrainerConfig,
                    data_transformation_artifacts:artifacts_entity.DataTransformationArtifact):
        try:
            
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifacts = data_transformation_artifacts

        except Exception as e:
            raise InsuranceException(e, sys)
        

    def random_forest_algorithm(self, x_train, y_train):
        try:

            rfr = RandomForestRegressor(max_depth=5, min_samples_split=12, n_estimators=300)
            rfr.fit(x_train, y_train)
            return rfr

        except Exception as e:
            raise InsuranceException(e, sys)
        

    def initiate_model_trainer(self)-> artifacts_entity.ModelTrainerArtifact:
        try:

            logging.info("Reading train and test data from data_transformation artifacts...")

            train_data_path = self.data_transformation_artifacts.transform_train_path
            test_data_path = self.data_transformation_artifacts.transform_test_path


            train_arr = utils.load_numpy_array_data(train_data_path)
            test_arr = utils.load_numpy_array_data(test_data_path)


            logging.info("splitting train and test data into x_train, x_test and y_train, y_test ...")

            x_train, y_train = train_arr[:, :-1] , train_arr[:, -1]
            x_test, y_test = test_arr[:, :-1] , test_arr[:, -1]

            logging.info(f"X_train shape is : {x_train.shape}")
            logging.info(f"x_test shape is : {x_test.shape}")

            logging.info("ready to fit data to model...")
            model = self.random_forest_algorithm(x_train=x_train, y_train=y_train)
            logging.info("data fitted to model...")


            # r2 score
            ry_pred_test = model.predict(x_test)
            r2_test_score = r2_score(y_true=y_test, y_pred=ry_pred_test)
            logging.info(f"predicted for x_test : {r2_test_score}")

            ry_pred_train = model.predict(x_train)
            r2_train_score = r2_score(y_true=y_train, y_pred=ry_pred_train)
            logging.info(f"predicted for x_train : {r2_train_score}")


#           mse
            msy_pred_train = model.predict(x_train)
            mse_train_score = mean_squared_error(y_true=y_train, y_pred=msy_pred_train)
            logging.info(f"predicted mse for x_train : {mse_train_score}")

            msy_pred_test = model.predict(x_test)
            mse_test_score = mean_squared_error(y_true=y_test, y_pred=msy_pred_test)
            logging.info(f"predicted mse for x_test : {mse_test_score}")

            # mae
            may_pred_train = model.predict(x_train)
            mae_train_score = mean_absolute_error(y_true=y_train, y_pred=may_pred_train)
            logging.info(f"predicted for mae x_train : {mae_train_score}")

            may_pred_test = model.predict(x_test)
            mae_test_score = mean_absolute_error(y_true=y_test, y_pred=may_pred_test)
            logging.info(f"predicted for  mae x_test : {mae_test_score}")


            # rmse
            rmy_pred_train = model.predict(x_train)
            rm_train_score = np.sqrt(mse_train_score)
            logging.info(f"predicted rmse for x_train : {rm_train_score}")

            rmy_pred_test = model.predict(x_test)
            rmy_test_score = np.sqrt(mse_test_score)
            logging.info(f"predicted for x_test : {rmy_test_score}")


            
            diff=abs(r2_train_score - r2_test_score)
            logging.info(f"calculating absolute diff between r2_train_score and r2_test_score, :  {diff}")

            logging.info("observing model performance whether is underfitted or overfitted...")
            if r2_test_score < self.model_trainer_config.expected_r2_score:
                raise Exception(f"model expected r2_score is : {self.model_trainer_config.expected_r2_score}, but got model r2_score is : {r2_test_score}")
            elif diff > self.model_trainer_config.overfitting_value:
                raise Exception(f"the absolute diff between train and test r2_score is : {diff} : model is overfitted...")
            print(f"accuracy : {r2_test_score} good, no underfitting, no overfitting")


            logging.info("save the model as a dill(pickle) file....")
            utils.save_object(file_path=self.model_trainer_config.model_path, 
                                obj=model)
            
            
            model_trainer_artifacts = artifacts_entity.ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path,
                r2_train_score=r2_train_score,
                r2_test_score=r2_test_score)
            

            return model_trainer_artifacts

        except Exception as e:
            raise InsuranceException(e,sys)




