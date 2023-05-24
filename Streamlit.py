import streamlit as st
st.set_page_config(layout="wide", page_title="Spring Connect", page_icon=":seedling:")
import streamlit.components.v1 as com
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from streamlit_capstone_functions import *
import os

spring_connect_logo = Image.open("ThumbnailSpring.png")
st.image(spring_connect_logo)
st.header("Welcome to Spring Connect")
st.subheader("Spring Connect is a platform for farmers to learn about their climate and adopt accordingly.")
tab1, tab2 = st.tabs(["Spring Community", "📈 Climate Dashboard"])
# get geolocation
location = get_geolocation()
latitude = location["coords"]["latitude"]
longitude = location["coords"]["longitude"]
script_path = os.path.abspath(__file__)

tab1.subheader("Tell us a little about your farm")

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

with tab2:
# get the location of the user
    # select one of these three locations in Rwanda
    fake_location_1 = Image.open("images/29.12, -2.53.png")
    fake_location_2 = Image.open("images/30.7, -2.12.png")
    fake_location_3 = Image.open("images/30.37, -1.2.png")
    st.write("Please select one of these locations in Rwanda")
    col1, col2, col3 = st.columns(3)
    col1.image(fake_location_1, width=400)
    col2.image(fake_location_2, width=400)
    col3.image(fake_location_3, width=400)
    
    # user can press a button under the image to select the location
    var_location = 0
    with col1:
        if st.button("Location 1"):
            st.write("You selected location 1")
            var_location = 1
    with col2:
        if st.button("Location 2"):
            st.write("You selected location 2")
            var_location = 2
    with col3:
        if st.button("Location 3"):
            st.write("You selected location 3")
            var_location = 3



    if var_location in [1,2,3]:
        st.write(f"Thank you for selecting a location, we are now loading the data. This is only a demo, in the real thing we would access our entire 200gb database using your current location which is {latitude}, {longitude}")
        if var_location == 1:
            path = "Image1/"
            data_path = os.path.join(os.path.dirname(script_path), "Image1/")
            csv_files = [f for f in os.listdir(data_path) if f.endswith(".csv")]
            dfs = {}
            for file in csv_files:
                df_name = os.path.splitext(file)[0]
                dfs[df_name] = load_data(os.path.join(data_path, file))
            
        if var_location == 2:
            path = "Image2"
            data_path = os.path.join(os.path.dirname(script_path), "Image2/")
            csv_files = [f for f in os.listdir(data_path) if f.endswith(".csv")]
            dfs = {}
            for file in csv_files:
                df_name = os.path.splitext(file)[0]
                dfs[df_name] = load_data(os.path.join(data_path, file))
            
        if var_location == 3:
            path = "Image3"
            data_path = os.path.join(os.path.dirname(script_path), "Image3/")
            csv_files = [f for f in os.listdir(data_path) if f.endswith(".csv")]
            dfs = {}
            for file in csv_files:
                df_name = os.path.splitext(file)[0]
                dfs[df_name] = load_data(os.path.join(data_path, file))
            
        st.subheader("Climate Predicitons")
        rcp_fig= plotly_rcp_graph(dfs["rcp45"], dfs["rcp45"])
        st.plotly_chart(figure_or_data = rcp_fig, theme= None, use_container_width=True)
        st.subheader("Temperatures")
        temp_fig = plotly_temperatures(dfs["Temp_max_24h"],dfs["Temp_mean_24h"], dfs["Temp_min_24h"])
        st.plotly_chart(figure_or_data = temp_fig, theme= None, use_container_width=True)

        oneplot_labels = ["Cloud_cover", "Precipitation", "Vapor Preassure"]
        
        st.subheader("Precipitation")
        prec_fig = plotly_one_stat_graph(dfs["percipitation"], oneplot_labels[1])
        st.plotly_chart(figure_or_data = prec_fig, theme= None, use_container_width=True)
        st.subheader("Vapor Preassure")
        vap_fig = plotly_one_stat_graph(dfs["preassure"], oneplot_labels[2])
        st.plotly_chart(figure_or_data = vap_fig, theme= None, use_container_width=True)
        st.subheader("Cloud Cover")
        cloud_fig = plotly_one_stat_graph(dfs["cloud_cover"], oneplot_labels[0])
        st.plotly_chart(figure_or_data = cloud_fig, theme= None, use_container_width=True)



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
    #script_path = os.path.abspath(__file__)

    # Construct the path to your data files using the script path
    # data_path = os.path.join(os.path.dirname(script_path), path)

    # # Get a list of all CSV files in the data folder
    # csv_files = [f for f in os.listdir(data_path) if f.endswith(".csv")]

    # # @st.cache_data
    # # def load_data(file):
    # #     df = pd.read_csv(file)
    # #     return df

    # dfs = {}
    # for file in csv_files:
    #     df_name = os.path.splitext(file)[0]
    #     dfs[df_name] = load_data(os.path.join(data_path, file))
    # st.write(dfs)

# df_names = list(dfs.keys())
# with tab1:
#     col1, col2, col3 = st.columns(3)

#     st.write("We will need to know your exact location to determine optimal crop composition and fertilizer type for your farm. Please allow us to access your location.")
#     selected_df_name = st.selectbox("Select a dataframe", df_names)
#     df = dfs[selected_df_name]
#     if selected_df_name in ["rcp45", "rcp85"]:
#         plot_creator_plotly = plot_creator_rcp_plotly
#         column_names = list(df.columns)
#         selected_column_name = st.selectbox("Select a column", column_names[3:])
#         title = st.text_input("Enter a title", f"{selected_column_name} vs time")
#         y_label = st.text_input("Enter a y-axis label", selected_column_name)
#     else:
#         column_names = list(df.columns)
#         #select the last column
#         selected_column_name = column_names[-1]
#         title = f"{selected_column_name} vs time"
#         y_label = selected_column_name
#     fig = plot_creator_plotly(lat=fake_lat, lon=fake_lon, df=df, column_name=selected_column_name, title=title, y_label=y_label)
#     #fig.update_layout(height=500, width=10000)
#     st.plotly_chart(figure_or_data = fig, theme= None, use_container_width=True)


    #if st.button("Display"):
    #    for df_name in df_names:
    #        if df_name != selected_df_name:
    #            fig = plot_creator_plotly(lat=latitude, lon=longitude, df=dfs[df_name], column_name=selected_column_name, title=title, y_label=y_label)
    #            st.plotly_chart(fig)
# get a satelit image

# get wather history for the location

# get rain history and weather forecast

#st.write("Your location is: ", location)
with tab1:
    st.subheader("Experts for you to connect with")

    col1, col2, col3, col4 = st.columns(4)
    portrait_1 = Image.open("Herveeeee.png")
    portrait_2 = Image.open("Festus.png")
    portrait_3 = Image.open("Youthika.png")
    portrait_4 = Image.open("GrantRound.png")
    company_logo_1 = Image.open("Mulika.png")
    company_logo_2 = Image.open("GreenPlanet.png")
    company_logo_3 = Image.open("Gates.png")
    
    
    
    col1.image(portrait_1, width=250)
    col2.image(portrait_2, width=250)
    col3.image(portrait_3, width=250)
    col1.write("Hervé Girihirwe, CEO/ Co-founder of Mulika Farms")
    col1.write("https://mulika.co/")
    col1.image(company_logo_1, width=100)
    col1.write("Mulika farms is a Rwandan based company that provides farmers with a digital  & analog platform to access markets by bypassing intermediaries.")
    col2.write("Festus Mwangi, CEO/ Co-founder of GPI2050")
    col2.write("https://gpi2050.org/")
    col2.image(company_logo_2, width=100)
    col2.write("The organization operates under a profound mission to heal, restore, and protect landscapes, thereby accelerating climate action at the grassroots level. Their focus is on vulnerable small-scale farming communities, pastoralists, and forest-dependent communities, supporting them in the restoration of degraded landscapes and fragile ecosystems.")
    col3.write("Youthica Chauhan, Ressearch Associate Bill & Melinda Gates Foundation")
    col3.write("https://www.gatesagone.org")
    col3.image(company_logo_3, width=50)

    col4.image(portrait_4, width=250)
    col4.write("Grant Meredith, former Citrus farmer in South Africa")
    col4.write("As a smalhold farmer, having to deal with a very delicate climate of the Gamtoos valley, and the competition with large scale farms, he has a deep understanding of how to differentate and be competitive as a smallhold farmer.")
    with col1:
        if st.button("Connect with Hervé"):
            st.write("Sorry, this feature is not available yet")

    with col2:
        if st.button("Connect with Festus"):
            st.write("Sorry, this feature is not available yet")

    with col3:
        if st.button("Connect with Youthica"):
            st.write("Sorry, this feature is not available yet")
    
    with col4:
        if st.button("Connect with Grant"):
            st.write("Sorry, this feature is not available yet")
    #col3.image(fake_location_3, width=400)
    

