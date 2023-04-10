from insurance_pred.logger import logging
from insurance_pred.exception import InsuranceException
import os, sys
from insurance_pred.utils import get_collection_as_df

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
        get_collection_as_df(database_name = "INSURANCE", collection_name = "INSURANCE_PROJECT")
    except Exception as e:
        print(e)
    