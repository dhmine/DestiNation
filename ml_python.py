# -*- coding: utf-8 -*-
"""
Created on 22-12-2022
@author: DHMINE Mohamed
"""

import streamlit as st
import pandas as pd
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np 
import openpyxl
import gc
from pathlib import Path
plt.style.use('ggplot')
import os
from PIL import Image
from ast import literal_eval
import base64
from matplotlib import pyplot as plt
from pandas import DataFrame
from pandas import Series
from pandas import concat
from pandas import read_csv
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import seaborn as sn
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')
import datetime 
from  STYLE import * 
from dateutil.relativedelta import relativedelta # to add days or years
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
from sklearn.metrics.pairwise import cosine_similarity
from langdetect import detect
from nltk.corpus import stopwords
import re
from nltk.corpus import stopwords
import geocoder
import folium
from folium import plugins
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import string
from sklearn.metrics.pairwise import cosine_similarity
import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
from streamlit_folium import st_folium
import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
from nltk.tokenize import word_tokenize
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('vader_lexicon')

######################################################## html styling ###########################################################
#call streamlit
st.set_page_config(page_title="System recommandation", page_icon="", layout="wide")
st.markdown('<style>body{background-color: #fbfff0}</style>',unsafe_allow_html=True)
st.markdown(html_header, unsafe_allow_html=True)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)




#pickle model for hotel attributes or tags
df4=pd.read_pickle('data.pkl')


#plotting function to map out the location


def create_map(df):

    #df = df.dropna(subset = ['lon', 'lat'])
    df['lon'] = df['lon'].astype(float)
    df['lat'] = df['lat'].astype(float)
    m = folium.Map(location=[df.lat.mean(), df.lon.mean()], zoom_start=8, tiles='OpenStreetMap')
    for _, row in df.iterrows():

        folium.CircleMarker(
            location= [row['lat'], row['lon']],
            radius =4,

           popup = F' Hotel : {row["name"]}, address : {row.address} , Rating : {row.rate}',


        ).add_to(m)
    return folium_static(m)


def get_recommendation_desc(description) :
    """

    :param description: user's description
    :return: recommendation hotels
    """
    if description == '' :
        print('Sorry there is no description. please write a real description')

    df4['rate'] = df4['rating'].astype(str)
    df = df4.dropna(subset = ['lon', 'lat'])
    temp = df.iloc[:1000]
    list_desc = list(temp['Description'])
    list_desc.append(description)#######
    embedding = model.encode(list_desc)
    similarity = cosine_similarity(
        [embedding[len(list_desc)-1]], embedding[:len(list_desc)-1])
    similarity = pd.DataFrame(similarity.T)
    temp['similarity'] = similarity
    temp = temp.sort_values(by='similarity', ascending=False)
    temp = temp.dropna(subset = ['lon', 'lat'])
    return temp[temp['similarity'] >= 0.6 ][['name','address','rate', 'description', 'lat', 'lon','similarity']]


def requirementbased(df, city,description):
    """

    :param city:
    :param description:
    :return:
    """
    df4['rate'] = df4['rating'].astype(str)
    df['City']=df['City'].str.lower()
    df['new_amenities']=df['new_amenities'].str.lower()
    #seperate to words
    description=description.lower()
    features_tokens=word_tokenize(description)
    #delete stop words from it
    sw = stopwords.words('english')
    lemm = WordNetLemmatizer()
    f1_set = {w for w in features_tokens if not w in sw}
    f_set=set()
    #add city
    for se in f1_set:
        f_set.add(lemm.lemmatize(se))
    reqbased=df[df['City']==city.lower()]
    reqbased=reqbased.set_index(np.arange(reqbased.shape[0]))
    cos=[];
    #tokenize amenities to words
    for i in range(reqbased.shape[0]):
        temp_tokens=word_tokenize(reqbased['new_amenities'][i])
        temp1_set={w for w in temp_tokens if not w in sw}
        temp_set=set()
    #intersection words between description and amenities
        for se in temp1_set:
            temp_set.add(lemm.lemmatize(se))
        rvector = temp_set.intersection(f_set)
        cos.append(len(rvector))
    reqbased['similarity']=cos
    reqbased['similarity'] = reqbased['similarity'].astype(int)
    reqbased=reqbased.sort_values(by=['similarity', 'rating'],ascending=False)
    reqbased = reqbased[['name','address','rate', 'lon', 'lat', 'similarity']].head(10)
    return reqbased[reqbased['similarity'] >0]


########################################################
all_amenities = []

for row in df4.amenities.values:
    a = literal_eval(row)
    all_amenities =  all_amenities + a 
amen_sum_set = set(all_amenities)



choice = st.radio(
    "the recommendation is based on : ",
    ('Description', 'Hotel Amenities'))

if choice == 'Description':
    form = st.form(key='sentiment-form')
    user_input = form.text_area('What kind of hotel do you want? (Write a description) ')
    submit = form.form_submit_button('Submit')

    if submit:
        result = get_recommendation_desc(user_input)
        st.write(result)
        try : 
        #st.map(result)
            create_map(result)
        except ValueError :
            print('error')
        
        #folium_static(result)
if choice == 'Hotel Amenities':
    selected_options = st.multiselect('Which amenity do you ?',all_amenities)
    selected_options = ' '.join(selected_options)
    if selected_options :
        form = st.form(key='sentiment-form1')
        user_input = form.text_area('Where do you want your hotel?')
        submit = form.form_submit_button('Click')
        if submit:
            result = requirementbased(df4, user_input, selected_options)
            st.write(result)
            try : 
                #st.map(result)
                create_map(result)
            except ValueError :
                print('error')




   

   
