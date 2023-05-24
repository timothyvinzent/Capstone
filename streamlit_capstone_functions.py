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


def plotly_temperatures(Temp_max_24h,Temp_mean_24h, Temp_min_24h):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=list(Temp_max_24h.time),
                y=list(Temp_max_24h.Temperature_Air_2m_Max_24h),
                name="Max Temperature 24h",
                line=dict(color="#F06A6A")))

    fig.add_trace(
        go.Scatter(x=list(Temp_max_24h.time),
                y=[Temp_max_24h.Temperature_Air_2m_Max_24h.mean()] * len(Temp_max_24h.index),
                name="Average Max Temperature 24h",
                visible=False,
                line=dict(color="#F06A6A", dash="dash")))

    fig.add_trace(
        go.Scatter(x=list(Temp_mean_24h.time),
                y=list(Temp_mean_24h.Temperature_Air_2m_Mean_24h),
                name="Mean Temperature 24h",
                line=dict(color="#33CFA5")))

    fig.add_trace(
        go.Scatter(x=list(Temp_mean_24h.time),
                y=[Temp_mean_24h.Temperature_Air_2m_Mean_24h.mean()] * len(Temp_mean_24h.index),
                name="Average Mean Temperature 24h",
                visible=False,
                line=dict(color="#33CFA5", dash="dash")))

    fig.add_trace(
        go.Scatter(x=list(Temp_min_24h.time),
                y=list(Temp_min_24h.Temperature_Air_2m_Min_24h),
                name="Min Temperature 24h",
                line=dict(color="#0000FF")))

    fig.add_trace(
        go.Scatter(x=list(Temp_min_24h.time),
                y=[Temp_min_24h.Temperature_Air_2m_Min_24h.mean()] * len(Temp_min_24h.index),
                name="Average Min Temperature 24h",
                visible=False,
                line=dict(color="#0000FF", dash="dash")))

    # Add Annotations and Buttons
    max_24h_annotations = [dict(x="2015-01-01",
                            y=Temp_max_24h.Temperature_Air_2m_Max_24h.mean(),
                            xref="x", yref="y",
                            text="Average Max:<br> %.3f" % Temp_max_24h.Temperature_Air_2m_Max_24h.mean(),
                            ax=0, ay=-40),
                        dict(x=Temp_max_24h.time[Temp_max_24h.Temperature_Air_2m_Max_24h.idxmax()],
                            y=Temp_max_24h.Temperature_Air_2m_Max_24h.max(),
                            xref="x", yref="y",
                            text="Highest Max:<br> %.3f" % Temp_max_24h.Temperature_Air_2m_Max_24h.max(),
                            ax=-40, ay=-40)]
    mean_daily_annotations = [dict(x="2015-05-01",
                            y=Temp_mean_24h.Temperature_Air_2m_Mean_24h.mean(),
                            xref="x", yref="y",
                            text="Average Mean:<br> %.3f" % Temp_mean_24h.Temperature_Air_2m_Mean_24h.mean(),
                            ax=0, ay=40),
                    dict(x=Temp_mean_24h.time[Temp_mean_24h.Temperature_Air_2m_Mean_24h.idxmax()],
                            y=Temp_mean_24h.Temperature_Air_2m_Mean_24h.max(),
                            xref="x", yref="y",
                            text="Highest Mean:<br> %.3f" % Temp_mean_24h.Temperature_Air_2m_Mean_24h.max(),
                            ax=0, ay=40)]
    min_daily_annotations = [dict(x="2015-05-01",
                            y=Temp_min_24h.Temperature_Air_2m_Min_24h.mean(),
                            xref="x", yref="y",
                            text="Average Min:<br> %.3f" % Temp_min_24h.Temperature_Air_2m_Min_24h.mean(),
                            ax=0, ay=40),
                    dict(x=Temp_min_24h.time[Temp_min_24h.Temperature_Air_2m_Min_24h.idxmin()],
                            y=Temp_min_24h.Temperature_Air_2m_Min_24h.min(),
                            xref="x", yref="y",
                            text="Lowest Min:<br> %.3f" % Temp_min_24h.Temperature_Air_2m_Min_24h.min(),
                            ax=0, ay=40)]

    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="None",
                        method="update",
                        args=[{"visible": [True, False, True, False, True, False]},
                            {"title": "Temperatures",
                                "annotations": []}]),
                    dict(label="24h Max",
                        method="update",
                        args=[{"visible": [True, True, False, False, False, False]},
                            {"title": "24h Max Temperatures",
                                "annotations": max_24h_annotations}]),
                    dict(label="24h Mean",
                        method="update",
                        args=[{"visible": [False, False, True, True, False, False]},
                            {"title": "24h Mean Temperatures",
                                "annotations": mean_daily_annotations}]),
                    dict(label="24h Min",
                        method="update",
                        args=[{"visible": [False, False, False, False, True, True]},
                            {"title": "24h Mean Temperatures",
                                "annotations": min_daily_annotations}]),
                    dict(label="All",
                        method="update",
                        args=[{"visible": [True, True, True, True, True, True]},
                            {"title": "24h Mean, Max & Min Temperatures",
                                "annotations": max_24h_annotations + mean_daily_annotations + min_daily_annotations}]),
                ]),
            )
        ])
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    # Set title
    fig.update_layout(title_text="Temperatures",template="plotly_white", xaxis_title='Time', yaxis_title= "Temperature (°C)", height=800)

    #fig.show()

    return fig


# now we make the same plot but for the percipitation, cloud cover, and pressure
def plotly_one_stat_graph(df, name):
    y_label = "test"
    if name == "Precipitation":
        y_label = "Precipitation (mm)"
    if name == "Cloud_cover":
        y_label = "Cloud Cover (%)"
    if name == "Vapor Preassure":
        y_label = "Pressure (hPa)"
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(x=list(df.time),
                y=list(df.iloc[: , -1]),
                name=f"Daily {name}",
                line=dict(color="#0000FF")))

    fig.add_trace(
        go.Scatter(x=list(df.time),
                y=[df.iloc[: , -1].mean()] * len(df.index),
                name=f"Average {name}",
                visible=False,
                line=dict(color="#0000FF", dash="dash")))
    
    max_annotations = [dict(x="2015-01-01",
                         y=df.iloc[: , -1].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % df.iloc[: , -1].mean(),
                         ax=0, ay=-40),
                    dict(x=df.time[df.iloc[: , -1].idxmax()],
                         y=df.iloc[: , -1].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % df.iloc[: , -1].max(),
                         ax=-40, ay=-40),
                    dict(x=df.time[df.iloc[: , -1].idxmin()],
                         y=df.iloc[: , -1].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % df.iloc[: , -1].min(),
                         ax=-40, ay=-40)
                         ]
    fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="None",
                     method="update",
                     args=[{"visible": [True, False]},
                           {"title": f"{name}",
                            "annotations": []}]),
                dict(label="All",
                     method="update",
                     args=[{"visible": [True, True]},
                           {"title": f"24h Mean, Max & Min {name}",
                            "annotations": max_annotations}]),
            ]),
        )
    ])
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    fig.update_layout(title_text=f"{name}",template="plotly_white",xaxis_title='Time', yaxis_title=y_label, height=800)

    return fig



# now we create the function fot the rcp45 and rcp 85 data
def plotly_rcp_graph(rcp45, rcp85):
    
    
    fig = go.Figure()
    # cloud cover
    #rcp 45
    fig.add_trace(
        go.Scatter(x=list(rcp45.time),
                y=list(rcp45.iloc[: , 4]),
                name=f"Daily cloud cover RCP45",
                line=dict(color="#0000FF")))
    #rcp 85
    fig.add_trace(
        go.Scatter(x=list(rcp85.time),
                y=list(rcp85.iloc[: , 4]),
                name=f"Daily cloud cover RCP85",
                line=dict(color="#F06A6A")))
    #precipitation
    #rcp 45
    fig.add_trace(
        go.Scatter(x=list(rcp45.time),
                y=list(rcp45.iloc[: , 5]),
                name=f"Daily precipitation RCP45",
                line=dict(color="#0000FF")))
    #rcp 85
    fig.add_trace(
        go.Scatter(x=list(rcp85.time),
                y=list(rcp85.iloc[: , 6]),
                name=f"Daily precipitation RCP85",
                line=dict(color="#F06A6A")))
    #vapor preassure
    #rcp 45
    fig.add_trace(
        go.Scatter(x=list(rcp45.time),
                y=list(rcp45.iloc[: , -1]),
                name=f"Daily vapor preassure RCP45",
                line=dict(color="#0000FF")))
    #rcp 85
    fig.add_trace(
        go.Scatter(x=list(rcp85.time),
                y=list(rcp85.iloc[: , -1]),
                name=f"Daily vapor preassure RCP85",
                line=dict(color="#F06A6A")))
    #temperature
    #rcp 45
    #max
    fig.add_trace(
        go.Scatter(x=list(rcp45.time),
                y=list(rcp45.iloc[: , 6]),
                name=f"Max Temperature 24h RCP45",
                line=dict(color="#0000FF")))
    #min
    fig.add_trace(
        go.Scatter(x=list(rcp45.time),
                y=list(rcp45.iloc[: , 7]),
                name=f"Min Temperature 24h RCP45",
                line=dict(color="#0000FF")))
    #mean
    fig.add_trace(
        go.Scatter(x=list(rcp45.time),
                y=list(rcp45.iloc[: , 8]),
                name=f"Mean Temperature 24h RCP45",
                line=dict(color="#0000FF")))
    # rcp 85
    #max
    fig.add_trace(
        go.Scatter(x=list(rcp85.time),
                y=list(rcp85.iloc[: , 7]),
                name=f"Max Temperature 24h RCP85",
                line=dict(color="#F06A6A")))
    #min
    fig.add_trace(
        go.Scatter(x=list(rcp85.time),
                y=list(rcp85.iloc[: , 8]),
                name=f"Min Temperature 24h RCP85",
                line=dict(color="#F06A6A")))
    #mean
    fig.add_trace(
        go.Scatter(x=list(rcp85.time),
                y=list(rcp85.iloc[: , 9]),
                name=f"Mean Temperature 24h RCP85",
                line=dict(color="#F06A6A")))

    
    cloud_annotations = [dict(x="2015-01-01",
                         y=rcp45.iloc[: , 4].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp45.iloc[: , 4].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , -1].idxmax()],
                         y=rcp45.iloc[: , 4].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp45.iloc[: , 4].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , 4].idxmin()],
                         y=rcp45.iloc[: , 4].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp45.iloc[: , 4].min(),
                         ax=-40, ay=-40),
                    dict(x="2015-01-01",
                         y=rcp85.iloc[: , 4].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp85.iloc[: , 4].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , 4].idxmax()],
                         y=rcp85.iloc[: , 4].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp85.iloc[: , 4].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , 4].idxmin()],
                         y=rcp85.iloc[: , 4].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp85.iloc[: , 4].min(),
                         ax=-40, ay=-40)
                         ]
    precip45_annotations = [dict(x="2015-01-01",
                         y=rcp45.iloc[: , 5].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp45.iloc[: , 5].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , 5].idxmax()],
                         y=rcp45.iloc[: , 5].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp45.iloc[: , 5].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , 5].idxmin()],
                         y=rcp45.iloc[: , 5].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp45.iloc[: , 5].min(),
                         ax=-40, ay=-40)]
    precip85_annotations = [dict(x="2015-01-01",
                         y=rcp85.iloc[: , 6].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp85.iloc[: , 6].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , 6].idxmax()],
                         y=rcp85.iloc[: , 6].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp85.iloc[: , 6].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , 6].idxmin()],
                         y=rcp85.iloc[: , 6].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp85.iloc[: , 6].min(),
                         ax=-40, ay=-40)]
    preassure_annotations = [dict(x="2015-01-01",
                         y=rcp45.iloc[: , -1].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp45.iloc[: , -1].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , -1].idxmax()],
                         y=rcp45.iloc[: , -1].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp45.iloc[: , -1].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , -1].idxmin()],
                         y=rcp45.iloc[: , -1].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp45.iloc[: , -1].min(),
                         ax=-40, ay=-40),
                    dict(x="2015-01-01",
                         y=rcp85.iloc[: , -1].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp85.iloc[: , -1].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , -1].idxmax()],
                         y=rcp85.iloc[: , -1].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp85.iloc[: , -1].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , -1].idxmin()],
                         y=rcp85.iloc[: , -1].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp85.iloc[: , -1].min(),
                         ax=-40, ay=-40)
                         ]
    temps45_annotations = [dict(x="2030-01-01",
                         y=rcp45.iloc[: , 6].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp45.iloc[: , 6].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , 6].idxmax()],
                         y=rcp45.iloc[: , 6].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp45.iloc[: , 6].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , 6].idxmin()],
                         y=rcp45.iloc[: , 6].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp45.iloc[: , 6].min(),
                         ax=-40, ay=-40),
                         dict(x="2040-01-01",
                         y=rcp45.iloc[: , 7].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp45.iloc[: , 7].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , 7].idxmax()],
                         y=rcp45.iloc[: , 7].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp45.iloc[: , 7].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , 7].idxmin()],
                         y=rcp45.iloc[: , 7].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp45.iloc[: , 7].min(),
                         ax=-40, ay=-40),
                         dict(x="2050-01-01",
                         y=rcp45.iloc[: , 8].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp45.iloc[: , 8].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , 8].idxmax()],
                         y=rcp45.iloc[: , 8].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp45.iloc[: , 8].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp45.time[rcp45.iloc[: , 8].idxmin()],
                         y=rcp45.iloc[: , 8].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp45.iloc[: , 8].min(),
                         ax=-40, ay=-40)]
    temps85_annotations = [dict(x="2035-01-01",
                         y=rcp85.iloc[: , 7].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp85.iloc[: , 7].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , 7].idxmax()],
                         y=rcp85.iloc[: , 7].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp85.iloc[: , 7].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , 7].idxmin()],
                         y=rcp85.iloc[: , 7].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp85.iloc[: , 7].min(),
                         ax=-40, ay=-40),
                         dict(x="2060-01-01",
                         y=rcp85.iloc[: , 8].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp85.iloc[: , 8].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , 8].idxmax()],
                         y=rcp85.iloc[: , 8].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp85.iloc[: , 8].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , 8].idxmin()],
                         y=rcp85.iloc[: , 8].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp85.iloc[: , 8].min(),
                         ax=-40, ay=-40),
                         dict(x="2080-01-01",
                         y=rcp85.iloc[: , 9].mean(),
                         xref="x", yref="y",
                         text="Average:<br> %.3f" % rcp85.iloc[: , 9].mean(),
                         ax=0, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , 9].idxmax()],
                         y=rcp85.iloc[: , 9].max(),
                         xref="x", yref="y",
                         text="Highest:<br> %.3f" % rcp85.iloc[: , 9].max(),
                         ax=-40, ay=-40),
                    dict(x=rcp85.time[rcp85.iloc[: , 9].idxmin()],
                         y=rcp85.iloc[: , 9].min(),
                         xref="x", yref="y",
                         text="Lowest:<br> %.3f" % rcp85.iloc[: , 9].min(),
                         ax=-40, ay=-40)]
    fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="Cloud Cover",
                     method="update",
                     args=[{"visible": [True, True, False, False, False, False, False, False, False, False, False, False]},
                           {"title": "Daily cloud cover forecast",
                            "annotations": cloud_annotations,"yaxis": {"title": "Cloud Cover (%)"}}]),
                dict(label="Precipitation RCP45",
                     method="update",
                     args=[{"visible": [False, False, True, False, False, False, False, False, False, False, False, False]},
                           {"title": "Daily precipitation forecast RCP45",
                            "annotations": precip45_annotations, "yaxis": {"title": "Precipitation (mm)"}}]),
                dict(label="Precipitation RCP85",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, False, False, False, False, False, False, False]},
                           {"title": "Daily precipitation forecast RCP85",
                            "annotations": precip85_annotations, "yaxis": {"title": "Precipitation (mm)"}}]),
                dict(label="Water Preassure",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, True, False, False, False, False, False, False]},
                           {"title": "Daily water preassure forecast",
                            "annotations": preassure_annotations, "yaxis": {"title": "Pressure (hPa)"}}]),
                dict(label="Temperature RCP45",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, True, True, True, False, False, False]},
                           {"title": "Temperature RCP 45 forecast",
                            "annotations": temps45_annotations, "yaxis": {"title": "Temperature (°C)"}}]),
                dict(label="Temperature RCP85",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, False, True, True, True]},
                           {"title": "Temperature RCP 85 forecast",
                            "annotations": temps85_annotations, "yaxis": {"title": "Temperature (°C)"}}]),
                dict(label="Temperature RCP45 & RCP85",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, True, True, True, True, True, True]},
                           {"title": "Temperature forecast",
                            "annotations": temps45_annotations + temps85_annotations, "yaxis": {"title": "Temperature (°C)"}}]),
                
            ]),
        )
    ])
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
    fig.update_layout(title_text="Climate predicitons based on a 2045 & 2085 scenario",template="plotly_white",xaxis_title='Time', height=800)

    return fig


