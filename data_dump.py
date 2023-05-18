import pymongo
import pandas as pd
import json

client = pymongo.MongoClient("mongodb+srv://vinod:insurance_prediction@cluster1.ixse1h4.mongodb.net/?retryWrites=true&w=majority")


DATA_FILE_PATH = "/home/vinod/projects/Insurance_prediction/insurance.csv"
DATABASE_NAME = "INSURANCE"
COLLECTION_NAME = "INSURANCE_PROJECT"

if __name__ == "__main__":
    data = pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns : {data.shape}")
    
    
    data.drop(columns="index", inplace=True)
    
    
    json_record = list(json.loads(data.T.to_json()).values())
    print(json_record[0])
    
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)