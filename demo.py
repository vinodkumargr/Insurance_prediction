from insurance_pred.pipeline.batch_prediction import strat_batch_prediction


file_path = "/home/vinod/projects/Insurance_prediction/insurance.csv"

if __name__ == "__main__":
    try:
        output = strat_batch_prediction(input_file_path=file_path)

    except Exception as e:
        print(e)