import streamlit as st
import pandas as pd
import pickle
import numpy as np

from sklearn.model_selection import GridSearchCV, cross_validate, cross_val_score, cross_val_predict
from sklearn.ensemble import RandomForestRegressor

raw_data = pd.read_csv('sao-paulo-properties-april-2019.csv')
raw_data = raw_data.iloc[:,:14]
cols = raw_data.iloc[:,1:14].columns

filename = 'finalized_model.sav'
hp_model = pickle.load(open(filename, 'rb'))

def get_dummies(data, df):

    data = pd.DataFrame(data, cols).T
    df_a = data.iloc[:,:10]

    df = df.iloc[:,1:14]

    dummies_frame = pd.get_dummies(df)

    df_b = pd.get_dummies(data)
    df_b = df_b.reindex(columns = dummies_frame.columns, fill_value=0).iloc[:,10:]
    
    df_final = pd.concat([df_a, df_b], axis=1)
    return df_final

def model_predict(param_list):
    
    X = pd.DataFrame(get_dummies(param_list, raw_data))
    predicted_price = hp_model.predict(X)

    return predicted_price

attrib_info = """
#### Attribute Information:
    - Condominium Price
    - Size (m²)
    - Number of Rooms
    - Number of Toilets
    - Number of Suits
    - Number of Parkings
    - Elevator: 0. No, 1.Yes
    - Furnished: 0. No, 1.Yes
    - Swimming Pool: 0. No, 1.Yes
    - New: 0. No, 1.Yes
    - District: Select one
    - Negotiation Type: Select one
    - Property Type: Default

"""

label_dict = {"No":0,"Yes":1}
negotiation_dict = {"rent":0,"sale":1}


def get_fvalue(val):
    feature_dict = {'No':0, 'Yes':1}
    for key, value in feature_dict.items():
        if val == key:
            return value

def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value


def run_ml_app():

    st.subheader('From ML Section')
    
    with st.expander('Attribute Info'):
        st.markdown(attrib_info)
    
    col1, col2 = st.columns(2)

    with col1:
        condo = st.number_input('Condominium Price R$')
        size = st.number_input('Size (m²)',step=1)
        rooms = st.number_input('Number of Rooms',step=1)
        toilets = st.number_input('Number of Toilets',step=1)
        has_elevator = st.radio('Elevator',['No','Yes'])
        is_furnished = st.radio('Furnished',['No','Yes'])

    with col2:
        suits = st.number_input('Number of Suits',step=1)
        parkings = st.number_input('Number of Parkings',step=1)
        district = st.selectbox("District",raw_data['District'].unique())
        negotiation_type = st.radio("Negotiation Type",['rent','sale'])
        has_swimpool = st.radio('Swimming Pool',['No','Yes'])
        is_new = st.radio('New',['No','Yes'])
        

    with st.expander('Selected Options'):
        result = {
            'condo':condo,
            'size':size,
            'rooms':rooms,
            'toilets':toilets,
            'suits':suits,
            'parkings':parkings,
            'has_elevator':has_elevator,
            'is_furnished':is_furnished,
            'has_swimpool':has_swimpool,
            'is_new':is_new,
            'district':district,
            'negotiation_type':negotiation_type,
            'property_type':'apartment'
        }
    
        st.write(result)

        encoded_result = []
        for i in result.values():
            if type(i) == int or type(i) == float:
                encoded_result.append(i)
            elif i in ['rent','sale']:
                encoded_result.append(i)
            elif i in raw_data['District'].unique():
                res = i.replace(' ','_')
                encoded_result.append(res)
            elif i == 'apartment':
                encoded_result.append('apartment')
            else:
                encoded_result.append(get_fvalue(i))

        st.write(encoded_result)

    with st.expander('Prediction Result'):
        single_sample = encoded_result
        prediction = model_predict(single_sample)

        st.success('The apartment is for {} for R${}'.format(result['negotiation_type'] ,round(prediction[0],2)))