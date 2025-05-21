import ast
import asyncio
from datetime import datetime
from faicons import icon_svg
import faicons
import folium.map
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import folium
from folium.plugins import HeatMap

from pathlib import Path

from data import database

import altair as alt
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from shiny import reactive
from shiny.express import render,input, ui
from shinywidgets import render_plotly, render_altair, render_widget


ui.tags.style(
    """
        .header-container {
        
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: black;
            height: 90px;
        }


        .logo-container {
            margin-right: 5px;
            height: 100%;
            padding: 10px;
        
        }

        .logo-container img {
            height: 60px;
        }

        .title-container h2 {
            color: white;
            padding: 5px;
            margin: 0;
        
        }




        body {

            background-color: #5e41aa;
        
        
        }


        .modebar{
            display: none;
        
        }

    """
)



ui.page_opts(window_title="GTFS DASHBOARD", fillable=False)





with ui.div(class_="header-container"):

    with ui.div(class_="title-container"):
        ui.h2("Toronto Collision Dashboard")

############################################
with ui.card():
    
    ui.card_header("General Information")
    with ui.layout_columns(col_widths={"sm": (4,4,4)}):

        with ui.value_box(
            showcase=faicons.icon_svg("calendar-days", width="50px"),
            theme="bg-gradient-green-red",
        ):
            "Start Date"

            @render.ui  
            def datestartfun():  
                return "January, 2014"  
            

        with ui.value_box(
            showcase=faicons.icon_svg("calendar-days", width="50px"),
            theme="bg-gradient-orange-red",
        ):
            "End Date"

            @render.ui  
            def dateendfun():  
                return "December, 2024"  
            


        with ui.value_box(
            showcase=faicons.icon_svg("car-burst", width="50px"),
            theme="bg-gradient-yellow-purple",
        ):
            "Number of Collisions"

            @render.ui
            def routefun():
                return len(database)


with ui.card(height="500px"):

    @render.ui
    def plot_network():
        m = folium.Map(location=[43.6, -79.4], zoom_start=10)
        HeatMap(data=database[['LAT_WGS84', 'LONG_WGS84']].values, radius=6).add_to(m)
        return m


