import streamlit as st
import pandas as pd
import numpy as np
import pickle as pkl

pickle_data = "/home/vinod/projects/Insurance_prediction/artifacts/data_transformation/Pre_process_model/single_pred_data.pkl"
pickle_model = "/home/vinod/projects/Insurance_prediction/artifacts/Model_pusher/saved_models/model.pkl"
transformer = "/home/vinod/projects/Insurance_prediction/artifacts/Model_pusher/saved_models/transformer.pkl"


model = pkl.load(open(pickle_model, 'rb'))
transformer = pkl.load(open(transformer, "rb"))

st.title("INSURANCE PREMIUM PREDICTION")


# Load the data for the dropdowns
data = pkl.load(open(pickle_data, 'rb'))


# Age column
age = st.number_input("AGE", step=1, value=1)
age = int(age)

# Sex column 
sex = st.selectbox('GENDER', data['sex'].unique())

# BMI column
bmi = st.number_input("BMI (Body Mass Index value)")

# children 
children = st.number_input("NUMBER OF CHILDREN YOU HAVE",step=1, value=1)
children = int(children)

# smoke column
smoker = st.selectbox('DO YOU SMOKE', data['smoker'].unique())


region = st.selectbox('YOUR REGION', data['region'].unique())



if st.button('PREDICT PREMIUM AMOUNT'):
    query_data = {'age': [age],
                  'sex': [sex],
                  'bmi': [bmi],
                  'children': [children],
                  'smoker': [smoker],
                  'region':[region]}
    
    if smoker == "Yes":
        smoker = 1
    else:
        smoker = 0

    df = pd.DataFrame(query_data, index=[0])

    df = transformer.transform(df)

    # Query point
    y_pred = model.predict(df)

    st.header(f"INSURANCE PREMIUM: {y_pred[0]}")
