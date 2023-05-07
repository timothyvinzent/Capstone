import streamlit as st
import streamlit.components.v1 as com
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
from PIL import Image


spring_connect_logo = Image.open("v7_23.png")
st.image(spring_connect_logo)



#st.title("Spring Connect")

st.header("Welcome to Spring Connect")

st.subheader("Spring Connect is a platform for connecting farmers to access the seed & fertilizer market and other services")

#st.divider()


tab1, tab2 = st.tabs(["🗃 Tell us more", "📈 Welcome"])


tab1.subheader("Please fill in the form below to tell us more about you")

st.write("We will need to know your exact location to determine optimal crop composition and fertilizer type for your farm. Please allow us to access your location.")

location = get_geolocation()

# get a satelit image

# get wather history for the location

# get rain history and weather forecast

st.write("Your location is: ", location)

tab2.subheader("What we have found for you")
