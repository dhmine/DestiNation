# test streamlit
from create_map import create_map
import streamlit as st
import pandas as pd
import numpy as np

from streamlit_folium import folium_static


st.write("Natural Heritage site")
text_input = st.text_input('Please Enter a location', "")



df = pd.read_csv('natural_heritage.csv')

st.map(df)

#%%

m = create_map(df)
folium_static(m)