# test streamlit
from create_map import create_map
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from streamlit_folium import folium_static

st.write("Event site")
df = pd.read_csv('new_event_data.csv')
# st.map(df)

### event type
event_list = tuple(df.new_type.unique()[1:])
city_list = tuple(df.addressLocality.value_counts().head(5).index)

text_input = st.text_input('Please Enter a location', "")
# option = st.selectbox( 'What type of event you  would like?',event_list)

start = datetime.strptime(str(datetime.today()).split()[0], '%Y-%m-%d')  # set default value
end = datetime.strptime(str(datetime.today()).split()[0], '%Y-%m-%d')  # set default value


# text_input = st.text_input('Please Enter start date and end date', "")
# start = st.date_input("Enter Start Date", value=start)
# end = st.date_input("Enter End Date", value=end)
def opon_file(file_name):
    pass


def filter_data(df, city, event, start, end):

    ndf = df[df.addressLocality == city]
    ndf = ndf[ndf.new_type == event]

    ndf = ndf[(pd.to_datetime(ndf.startDate).dt.date >= start) & (pd.to_datetime(ndf.endDate).dt.date  <= end)]

    return ndf

    return ndf


with st.form(key='columns_in_form'):
    col1, col2 = st.columns(2)
    with col1:
        city = st.selectbox('Select location', city_list, key=0)
        start = st.date_input("Enter Start Date", value=start, key=3)
    with col2:
        event = st.selectbox('What type of event you  would like?', event_list, key=1)
        end = st.date_input("Enter End Date", value=end, key=4)
    submitted = st.form_submit_button('Submit')

    ndf = filter_data(df, city, event, start, end)



    #st.map(ndf)
    m = create_map(ndf)
    folium_static(m)
    st.table(ndf[['label', 'startDate', 'endDate']])

# %%

# m = create_map(df)
# folium_static(m)
