import streamlit as st
st.set_page_config(layout="wide", page_title="Spring Connect", page_icon=":seedling:")
import streamlit.components.v1 as com
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_capstone_functions import plot_creator_plotly, plot_creator_rcp_plotly
import os

spring_connect_logo = Image.open("ThumbnailSpring.png")
st.image(spring_connect_logo)
st.header("Welcome to Spring Connect")
st.subheader("Spring Connect is a platform for connecting farmers to access the seed & fertilizer market and other services")
tab1, tab2 = st.tabs(["Monitor your Climate", "📈 Connect with the community"])
# get geolocation
location = get_geolocation()
latitude = location["coords"]["latitude"]
longitude = location["coords"]["longitude"]

tab1.subheader("Please tell us a little about your farm")
with tab1:
# get the location of the user
    # select one of these three locations in Rwanda
    fake_location_1 = Image.open("images/29.12, -2.53.png")
    fake_location_2 = Image.open("images/30.7, -2.12.png")
    fake_location_3 = Image.open("images/30.37, -1.2.png")
    col1, col2, col3 = st.columns(3)
    col1.image(fake_location_1, width=200)
    col2.image(fake_location_2, width=200)
    col3.image(fake_location_3, width=200)
    st.write("Please select one of these locations in Rwanda")
    # user can press a button under the image to select the location
    with col1:
        if st.button("Select"):
            st.write("You selected location 1")
    with col2:
        if st.button("Select"):
            st.write("You selected location 2")
    with col3:
        if st.button("Select"):
            st.write("You selected location 3")

    st.write("Your location is: ", latitude, longitude)
    fake_lat = 47.43478468940344 
    fake_lon = 9.383939772613207
# read the data from the csv files
# path = "Capstone/Streamlit small/"
# path_lst = os.listdir(path)

## make a selection for different location, we just build in the selector, based on the dataset we collect we display a different image at the top of the location
## Also integrate some intelligence on the stats of the time series
## add in some examples on the ideal crop timing, could use fake values for now
## integrate a market analysis tool for the production and supply of different crop types in your region using FAO stat
## the get location has to be faked for now to be able to deploy on streamlit share
## create a connect to experts page, confrence date, match making functionality, maybe we could fake it a little bit for now
## Create a fake page on the current state of spring and the stuff they are doing
## create a fake page about the mockups, or just put the presentation in there

# @st.cache_data
# def load_data(file):
#     df = pd.read_csv(file)
#     return df

# dfs = {}
# for file in path_lst:
#     df_name = os.path.splitext(file)[0]
#     dfs[df_name] = load_data(f"{path}/{file}")

# Get the absolute path of your script
script_path = os.path.abspath(__file__)

# Construct the path to your data files using the script path
data_path = os.path.join(os.path.dirname(script_path), "Streamlit small")

# Get a list of all CSV files in the data folder
csv_files = [f for f in os.listdir(data_path) if f.endswith(".csv")]

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

dfs = {}
for file in csv_files:
    df_name = os.path.splitext(file)[0]
    dfs[df_name] = load_data(os.path.join(data_path, file))

df_names = list(dfs.keys())
with tab1:
    col1, col2, col3 = st.columns(3)

    st.write("We will need to know your exact location to determine optimal crop composition and fertilizer type for your farm. Please allow us to access your location.")
    selected_df_name = st.selectbox("Select a dataframe", df_names)
    df = dfs[selected_df_name]
    if selected_df_name in ["rcp45", "rcp85"]:
        plot_creator_plotly = plot_creator_rcp_plotly
        column_names = list(df.columns)
        selected_column_name = st.selectbox("Select a column", column_names[3:])
        title = st.text_input("Enter a title", f"{selected_column_name} vs time")
        y_label = st.text_input("Enter a y-axis label", selected_column_name)
    else:
        column_names = list(df.columns)
        #select the last column
        selected_column_name = column_names[-1]
        title = f"{selected_column_name} vs time"
        y_label = selected_column_name
    fig = plot_creator_plotly(lat=fake_lat, lon=fake_lon, df=df, column_name=selected_column_name, title=title, y_label=y_label)
    #fig.update_layout(height=500, width=10000)
    st.plotly_chart(figure_or_data = fig, theme= None, use_container_width=True)


    #if st.button("Display"):
    #    for df_name in df_names:
    #        if df_name != selected_df_name:
    #            fig = plot_creator_plotly(lat=latitude, lon=longitude, df=dfs[df_name], column_name=selected_column_name, title=title, y_label=y_label)
    #            st.plotly_chart(fig)
# get a satelit image

# get wather history for the location

# get rain history and weather forecast

#st.write("Your location is: ", location)

tab2.subheader("What we have found for you")
