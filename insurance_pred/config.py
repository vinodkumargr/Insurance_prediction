import pymongo
import pandas as pd
import numpy as np
import json
import os, sys
from dataclasses import dataclass


class EnvironmentVariable:
    mongo_db_url = os.getenv("MONGO_DB_URL")
    
    
env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
TARGET_COLUMN = "charges"
print(f"mongo client: {mongo_client}")