import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.graph_objs as go
import streamlit as st


def check_point_within_range(u_lat, u_lon, lat_range, long_range):
    if lat_range[0] <= u_lat <= lat_range[1] and long_range[0] <= u_lon <= long_range[1]:
        return True
    else:
        return False

def closest(lst, n):
    return min(lst, key=lambda x: abs(x-n))



def plot_creator_plotly(lat, lon, df, column_name, title, y_label):
    switzerland_lat_range = (45.8172, 47.8087)
    switzerland_long_range = (5.9569, 10.4922)

    france_lat_range = (41.3712, 51.0918)
    france_long_range = (-5.1428, 9.5600)

    rwanda_lat_range = (-2.8400, -1.0471)
    rwanda_long_range = (28.8614, 30.8958)

    u_lat = lat
    u_lon = lon

    country_loc = [(switzerland_lat_range, switzerland_long_range), (france_lat_range, france_long_range), (rwanda_lat_range, rwanda_long_range)]
    countries = ['Switzerland', 'France', 'Rwanda']

    checkpoint = False
    your_country= []

    for i in range(len(country_loc)):
        if check_point_within_range(u_lat, u_lon, country_loc[i][0], country_loc[i][1]) == True:
            checkpoint = True
            your_country.append(countries[i])
            continue
        else:
            continue
    if checkpoint == False:
        print("Your location is not within the range of the data we have")
        st.write("Your location is not within the range of the data we have")
    else:
        print(f"Your location is within the range of {your_country[0]}")
        st.write(f"Your location is within the range of {your_country[0]}")

    df_filtered = df[(df['lon'].round(1) == round(u_lon, 1)) & (df['lat'].round(1) == round(u_lat, 1))]

    df_filtered['time'] = pd.to_datetime(df_filtered['time'], format='%Y-%m-%d %H:%M:%S')

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_filtered['time'], y=df_filtered[column_name], mode='lines', name='Temperature'))

    fig.update_layout(title=title,
                      xaxis_title='Time',
                      yaxis_title=y_label)

    return fig

import pandas as pd
import plotly.graph_objs as go

def plot_creator_rcp_plotly(lat, lon, df, column_name, title, y_label):
    switzerland_lat_range = (45.8172, 47.8087)
    switzerland_long_range = (5.9569, 10.4922)

    france_lat_range = (41.3712, 51.0918)
    france_long_range = (-5.1428, 9.5600)

    rwanda_lat_range = (-2.8400, -1.0471)
    rwanda_long_range = (28.8614, 30.8958)

    u_lat = lat
    u_lon = lon

    country_loc = [(switzerland_lat_range, switzerland_long_range), (france_lat_range, france_long_range), (rwanda_lat_range, rwanda_long_range)]
    countries = ['Switzerland', 'France', 'Rwanda']

    checkpoint = False
    your_country= []

    for i in range(len(country_loc)):
        if check_point_within_range(u_lat, u_lon, country_loc[i][0], country_loc[i][1]) == True:
            checkpoint = True
            your_country.append(countries[i])
            continue
        else:
            continue
    if checkpoint == False:
        print("Your location is not within the range of the data we have")
    else:
        print(f"Your location is within the range of {your_country[0]}")

    df_filtered = df[(df["lon"] == closest(df["lon"].unique().tolist(), u_lon)) & (df["lat"] == closest(df["lat"].unique().tolist(), u_lat))]

    df_filtered['time'] = pd.to_datetime(df_filtered['time'], format='%Y-%m-%d %H:%M:%S')

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_filtered['time'], y=df_filtered[column_name], name=column_name))

    fig.update_layout(title=title,
                      xaxis_title='Time',
                      yaxis_title=y_label)

    return fig

