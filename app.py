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
            background-color: #001861;  
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
            font-weight: bold;
            margin-bottom: 4px;
            color: black;
        }

        .vb-value {
            font-size: 16px;
            font-weight: 600;
        }
        .vb-small {
            
            min-height: 63px !important;
            height: 63px !important;
        }
        .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100px;
            padding: 10px;
            margin: 0px !important;
        }
        .logo-container {
            margin: 0px !important;
            height: 100%;
            padding: 10px;
        
        }
        .logo-container img {
            height: 100px;
            margin: 0px !important;
           
        }

    """
)


ui.page_opts(window_title="Toronto Collision Dashboard", fillable=True)





with ui.sidebar():

    with ui.div(class_="header-container"):
        with ui.div(class_="logo-container"):
            ui.a(
                ui.img(src="Logo.png"),  # adjust height as needed
                href="https://data.torontopolice.on.ca/pages/open-data",
                target="_blank"
            )
    ui.input_select(
        "year", "Select Year",
        ["All"] + [str(y) for y in range(2014, 2025)],
        selected="All"
    )


    ui.input_select(
        "season", "Select Season",
        ["All", "Winter", "Spring", "Summer", "Fall"],
        selected="All"
    )


    ui.input_select(
        "month", "Select Month",
        ["All"] + [calendar.month_name[m] for m in range(1, 13)],
        selected="All"
    )

with ui.div(class_="custom-nav-wrapper"):
        
    with ui.navset_pill(id="tab"): 
        
        with ui.nav_panel("Overview"):
            with ui.layout_columns(col_widths={"sm": (4, 4, 4)}):

                with ui.value_box(
                    showcase=icon_svg("calendar-days", width="40px"),
                    theme="bg-gradient-green-red",
                    class_="vb-small"
                ):
                    ui.div("Start Date", class_="vb-title")
                    
                    @render.ui
                    def datestartfun():
                        return ui.div("January, 2014", class_="vb-value")
                    
                with ui.value_box(
                    showcase=icon_svg("calendar-days", width="40px"),
                    theme="bg-gradient-green-red",
                    class_="vb-small"
                ):
                    ui.div("End Date", class_="vb-title")

                    @render.ui
                    def dateendfun():
                        return ui.div("December, 2024", class_="vb-value")

                with ui.value_box(
                    showcase=icon_svg("car-burst", width="40px"),
                    theme="bg-gradient-orange-red",
                    class_="vb-small"
                ):
                    ui.div("Number of Collisions", class_="vb-title")

                    @render.ui
                    def routefun():
                        return ui.div(str(len(database)), class_="vb-value")
                        
            # Step 5: Render map in Shiny Express
       
            with ui.layout_columns(col_widths={"sm": (6, 6)}):
                    
                with ui.card(full_screen=True, height="310px"):

                    @render.ui
                    def plot_network():
                        # Step 2: Create a Folium Map centered around Toronto
                        m = folium.Map(location=[43.73, -79.3], zoom_start=10, tiles="cartodbpositron")

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
                    
                with ui.card(height="310px"):
                    ui.card_header("Total Collisions by Year")

                    @render.plot
                    def collision_all_plot():
             

                        collisions_per_year = database.groupby('OCC_YEAR').size().sort_index()

                        collisions_per_year.plot(kind='bar', color='orange')

                        plt.xlabel('Year', fontsize=8)
                        plt.ylabel('Collision Count', fontsize=8)
                        plt.xticks(rotation=0, fontsize=6)
                        plt.yticks(fontsize=8)

                        plt.tight_layout()
           
                       
                with ui.card(height="310px"):
                    ui.card_header("Total Fatals by Year")

                    @render.plot
                    def fatal_all_plot():
                        # Filter rows where fatal collisions are greater than 0
                        filtered_df = database[database['FATALITIES'] > 0]

                        # Group by year and count the number of rows per year
                        fatalities_per_year = filtered_df.groupby('OCC_YEAR')['FATALITIES'].sum().sort_index()

                        # Plotting
                        fatalities_per_year.plot(kind='bar', color='crimson')

                        # Customize fonts
                
                        plt.xlabel('Year', fontsize=8)
                        plt.ylabel('Fatal Count', fontsize=8)
                        plt.xticks(rotation=0, fontsize=6)
                        plt.yticks(fontsize=8)

                        plt.tight_layout()



                with ui.card(height="310px"):
                    ui.card_header("Percentage of Runaway by Year")

                    @render.plot
                    def runway_all_plot():
    
                        # Total collisions per year
                        total_per_year = database.groupby('OCC_YEAR').size()

                        # Runaway collisions per year
                        runaway_per_year = database[database['FTR_COLLISIONS'] > 0].groupby('OCC_YEAR').size()

                        # Calculate percentage (ensure same index)
                        percentage_runaway_per_year = (runaway_per_year / total_per_year) * 100

                        # Plot as a line chart
                        
                        plt.plot(percentage_runaway_per_year.index, percentage_runaway_per_year.values, marker='o', color='purple', linestyle='-')

                     
                        plt.xlabel('Year', fontsize=8)
                        plt.ylabel('Percentage (%)', fontsize=8)
                        plt.xticks(rotation=0, fontsize=6)
                        plt.yticks(fontsize=8)

                        plt.grid(True, linestyle='--', linewidth=0.5)
                        plt.tight_layout()

        with ui.nav_panel("Division-based Analysis"):
            "Panel B content"

        with ui.nav_panel("Neighborhood-based Analysis"):
            "Panel C content"

