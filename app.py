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
            padding: 0px !important;
            margin: 0px !important;
        }


        .title-container h3 {
            color: white;
            padding: 0px !important;
            margin: 0px !important;
        
        }




        body {

            background-color: #5e41aa;
            padding: 0px !important;
            Margin: 0px !important;
        
        
        }

        .card {
            background-color: white;
            padding: 0px !important;
            border-radius: 0px;
            box-shadow: 2px 2px 10px rgba(0, 250, 0, 0.1);
            margin: 0px !important
        }
        .modebar{
            display: none;
        
        }
        .info-gen-css {
            font-size: 16px !important; /* Adjust the size as needed */
            color: white !important;
            display: flex !important; /* Enables centering */
            align-items: center !important; /* Centers vertically */
            justify-content: center !important; /* Centers horizontally */
            text-align: center !important; /* Ensures text alignment */
            font-weight: bold !important; /* Makes the text bold */
            background-color: purple !important;
        }
        .sidebar {
            background-color: white !important;
        }

    """
)



ui.page_opts(title="Toronto Collision", fillable=True)









with ui.sidebar(open="desktop"):

    ui.input_checkbox_group(
        "time",
        "Food service",
        ["Lunch", "Dinner"],
        selected=["Lunch", "Dinner"],
        inline=True,
    )
    ui.input_action_button("reset", "Reset filter")

    
############################################
with ui.card():
    
    ui.card_header("General Information", class_="info-gen-css")
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


with ui.card(full_screen=True, height="500px"):

    @render.ui
    def plot_network():
        m = folium.Map(location=[43.6, -79.4], zoom_start=10)
        HeatMap(data=database[['LAT_WGS84', 'LONG_WGS84']].values, radius=6).add_to(m)
        return m


