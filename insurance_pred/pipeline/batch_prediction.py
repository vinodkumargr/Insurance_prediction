from insurance_pred.logger import logging
from insurance_pred.exception import InsuranceException
from typing import Optional
import os, sys
import pandas as pd
import numpy as np
from insurance_pred.predictor import ModelResolver
from insurance_pred import config
from insurance_pred import utils


PREDICTION_DIR = "Prediction"


def strat_batch_prediction(input_file_path):
    try:
        
        os.makedirs(PREDICTION_DIR, exist_ok=True)
        model_resolver=ModelResolver(model_registry="saved_models")

        # load data:
        data = pd.read_csv(input_file_path)
        data = data.copy()
        data = data.dropna(axis=0)

        data['charges'] = data.charges.astype(int)


        transformer = utils.load_object(file_path=model_resolver.get_latest_save_transform_path())
        
        #input_feature_names = list(transformer.get_feature_names_out())
        #input_arr = transformer.transform(data[input_feature_names])

        input_arr = transformer.transform(data)

        model = utils.load_object(file_path=model_resolver.get_latest_save_model_path())
        prediction = model.predict(input_arr)

        data['prediction'] = prediction

        prediction_file_name = os.path.join(PREDICTION_DIR, "prediction_file.csv")
        data.to_csv(path_or_buf=prediction_file_name, index=False, header=True)

        return prediction_file_name

    except Exception as e:
        raise InsuranceException(e, sys) from e