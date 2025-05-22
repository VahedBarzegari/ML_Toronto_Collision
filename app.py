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
import branca.colormap as cm
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster

from pathlib import Path

from data import database, hex_gdf

import altair as alt
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from shiny import reactive
from shiny.express import render,input, ui
from shinywidgets import render_plotly, render_altair, render_widget
import geopandas as gpd
import pandas as pd
import folium
from shapely.geometry import Point
import h3
import h3
from shapely.geometry import Polygon
from shiny.express import ui, render

ui.tags.style(
    """





        body {

            background-color: white;
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
            background-color: lightgray !important;
        }
        .custom-nav-wrapper {
            background-color: orange;  /* light blue-gray */
            padding: 10px;
            border-radius: 8px;
            margin: 0px;
        }
        .nav-pills .nav-link {
            background-color: #f8f9fa;   /* Light gray background */
            color: #000;                 /* Black text */
            border: 1px solid #ccc;      /* Light border */
            margin-bottom: 10px;
            margin-right: 10px !important;
            font-weight: bold;
        }

        .nav-pills .nav-link.active {
            background-color: #007bff;   /* Bootstrap primary blue for active */
            color: white;
        }

        .nav-pills .nav-link:hover {
            background-color: #e2e6ea;   /* Slightly darker on hover */
            color: #000;
        }
        .vb-title {
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 4px;
        }

        .vb-value {
            font-size: 16px;
            font-weight: 600;
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

with ui.div(class_="custom-nav-wrapper"):
        
    with ui.navset_pill(id="tab"): 
        
        with ui.nav_panel("General Information"):
            with ui.layout_columns(col_widths={"sm": (4, 4, 4)}):

                with ui.value_box(
                    showcase=icon_svg("calendar-days", width="40px"),
                    theme="bg-gradient-green-red",
                ):
                    ui.div("Start Date", class_="vb-title")

                    @render.ui
                    def datestartfun():
                        return ui.div("January, 2014", class_="vb-value")

                with ui.value_box(
                    showcase=icon_svg("calendar-days", width="40px"),
                    theme="bg-gradient-orange-red",
                ):
                    ui.div("End Date", class_="vb-title")

                    @render.ui
                    def dateendfun():
                        return ui.div("December, 2024", class_="vb-value")

                with ui.value_box(
                    showcase=icon_svg("car-burst", width="40px"),
                    theme="bg-gradient-yellow-purple",
                ):
                    ui.div("Number of Collisions", class_="vb-title")

                    @render.ui
                    def routefun():
                        return ui.div(str(len(database)), class_="vb-value")
                        
            # Step 5: Render map in Shiny Express
       

            with ui.card(full_screen=True, height="500px"):

                @render.ui
                def plot_network():
                    # Step 2: Create a Folium Map centered around Toronto
                    m = folium.Map(location=[43.6, -79.4], zoom_start=10, tiles="cartodbpositron")

                    # Step 3: Create a color scale
                    max_val = hex_gdf['collision_count'].max()
                    colormap = cm.linear.YlOrRd_09.scale(0, max_val)
                    colormap.caption = 'Number of Collisions'
                    colormap.add_to(m)

                    # Step 4: Add each hexagon to the map
                    for _, row in hex_gdf.iterrows():
                        # Color based on collision count
                        color = colormap(row['collision_count'])
                        
                        # Add to map
                        folium.GeoJson(
                            row['geometry'],
                            style_function=lambda feature, color=color: {
                                'fillColor': color,
                                'color': 'black',
                                'weight': 0.5,
                                'fillOpacity': 0.6
                            },
                            tooltip=folium.Tooltip(f"Collisions: {row['collision_count']}"),
                        ).add_to(m)


                    return m
        with ui.nav_panel("B"):
            "Panel B content"

