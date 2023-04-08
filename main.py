from insurance_pred.logger import logging
from insurance_pred.exception import InsuranceException
import os, sys


def test_logger_and_exception():
    try:
        logging.info("Starting test_logger_and_exception")
        result = 3 / 0
        print(result)
        logging.info("Ending point of test_logger_and_excpetion")
    except Exception as e:
        logging.debug(str(e))
        raise InsuranceException(e, sys)
    
    
if __name__ == "__main__":
    try:
        test_logger_and_exception()
    except Exception as e:
        print(e)
    