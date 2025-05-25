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
from folium import Choropleth
from pathlib import Path

from data import database, hex_gdf, DIV_geo

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
            box-shadow: 2px 2px 10px rgba(0, 250, 0, 0.3);
            margin: 0px !important;
            border-color: black;
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
            background-color: yellow;   /* Slightly darker on hover */
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
    ui.input_selectize(
        "year", "Select Year",
        ["All"] + [str(y) for y in range(2014, 2025)],
        multiple=True,
        selected="All"
    )





    ui.input_selectize(
        "month", "Select Month",
        ["All"] + [calendar.month_name[m] for m in range(1, 13)],
        multiple=True,
        selected="All"
    )

    ui.input_selectize(
        "day", "Select Day of Week",
        ["All"] + ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        multiple=True,
        selected="All"
    )

    ui.input_selectize(
        "timerange", 
        "Select Time Range", 
        ["All", "Morning", "Midday", "Evening", "Night"], 
        multiple=True,
        selected=["All"]
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
                    
                with ui.card(full_screen=True, height="350px"):

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
                    
                with ui.card(full_screen=True, height="350px"):
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
           
                       
                with ui.card(full_screen=True, height="310px"):
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



                with ui.card(full_screen=True, height="310px"):
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

            with ui.layout_columns(col_widths={"sm": (12)}):

                with ui.layout_columns(col_widths={"sm": (6,6)}):
                    with ui.card(full_screen=True, height='350px'):
                            
                            @render.data_frame  
                            def insights_df():

                                c = str(input.year())

                                if 'All' in c:
                                    database1 = database.copy()
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [int(x) for x in c_tuple if x.isdigit()] 
                                    database1 = database[database['OCC_YEAR'].isin(b)]

                                c = str(input.month())

                                if 'All' in c:
                                    database1 = database1.copy()
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [x for x in c_tuple] 
                                    database1 = database1[database1['OCC_MONTH'].isin(b)]

                                    
                                c = str(input.day())

                                if 'All' in c:
                                    database1 = database1.copy()
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [x for x in c_tuple] 
                                    database1 = database1[database1['OCC_DOW'].isin(b)]

                                c = str(input.timerange())

                                if 'All' in c:
                                    database1 = database1.copy()
                                else:

                                    c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                    b = [x for x in c_tuple] 
                                    database1 = database1[database1['Time Range'].isin(b)]


                                return render.DataGrid(database1.head(100), selection_mode="row")  


                    with ui.card(full_screen=True, height='350px'):
                        with ui.card_header(""):

                            ICONS = {
                                "ellipsis": faicons.icon_svg("ellipsis"),
                            }
                            with ui.popover(title="Measure", placement="top"):
                                ICONS["ellipsis"]
                                ui.input_radio_buttons(
                                    "filter_map_Div",
                                    None,
                                    ["Collisions", "Fatals"],
                                    inline=True,
                                )

                        @render.ui
                        def map_DIV():


                            c = str(input.year())

                            if 'All' in c:
                                database1 = database
                            else:

                                c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                b = [int(x) for x in c_tuple if x.isdigit()] 
                                database1 = database[database['OCC_YEAR'].isin(b)]

                            c = str(input.month())

                            if 'All' in c:
                                database1 = database1.copy()
                            else:

                                c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                b = [x for x in c_tuple] 
                                database1 = database1[database1['OCC_MONTH'].isin(b)]

                            c = str(input.day())

                            if 'All' in c:
                                database1 = database1.copy()
                            else:

                                c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                b = [x for x in c_tuple] 
                                database1 = database1[database1['OCC_DOW'].isin(b)]

                            c = str(input.timerange())

                            if 'All' in c:
                                database1 = database1.copy()
                            else:

                                c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                b = [x for x in c_tuple] 
                                database1 = database1[database1['Time Range'].isin(b)]


                            if input.filter_map_Div() == "Fatals":
                                # Sum fatalities per DIV
                                division_data = database1.groupby("DIV")["FATALITIES"].sum().reset_index()
                                division_data.columns = ["DIV", "Number of Fatalities"]
                                value_column = "Number of Fatalities"
                                color = "Reds"
                                legend_name = "Number of Fatalities"
                            else:
                                # Count number of collisions per DIV
                                division_data = database1["DIV"].value_counts().reset_index()
                                division_data.columns = ["DIV", "Number of Collisions"]
                                value_column = "Number of Collisions"
                                color = "YlOrRd"
                                legend_name = "Number of Collisions"

                            # Merge with GeoDataFrame
                            merged = DIV_geo.merge(division_data, on="DIV")
                            merged = merged.to_crs(epsg=4326)

                            # Initialize Folium map
                            m = folium.Map(location=[43.7, -79.4], zoom_start=10, tiles="cartodbpositron")

                            # Choropleth layer
                            Choropleth(
                                geo_data=merged,
                                data=merged,
                                columns=["DIV", value_column],
                                key_on="feature.properties.DIV",
                                fill_color=color,
                                fill_opacity=0.9,
                                line_opacity=0.6,
                                legend_name=legend_name,
                            ).add_to(m)

                            # Tooltip with clear labels
                            folium.GeoJson(
                                merged,
                                name="Divisions",
                                tooltip=folium.features.GeoJsonTooltip(
                                    fields=["DIV", value_column],
                                    aliases=["Division:", f"{legend_name}:"],
                                    localize=True
                                ),
                                style_function=lambda x: {"fillOpacity": 0, "weight": 0}
                            ).add_to(m)

                            return m

                with ui.layout_columns(col_widths={"sm": (4,4,4)}):

                    with ui.card(full_screen=True, height='350px'):

                        ICONS = {
                            "ellipsis": faicons.icon_svg("ellipsis"),
                        }
                        with ui.popover(title="Measure", placement="top"):
                            ICONS["ellipsis"]
                            ui.input_radio_buttons(
                                "filter_worstDiv",
                                None,
                                ["Collisions", "Fatals"],
                                inline=True,
                            )
                        
                        @render.plot
                        def top_division_plot():

                            c = str(input.year())

                            if 'All' in c:
                                database1 = database
                            else:

                                c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                b = [int(x) for x in c_tuple if x.isdigit()] 
                                database1 = database[database['OCC_YEAR'].isin(b)]

                            c = str(input.month())

                            if 'All' in c:
                                database1 = database1.copy()
                            else:

                                c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                b = [x for x in c_tuple] 
                                database1 = database1[database1['OCC_MONTH'].isin(b)]


                            c = str(input.day())

                            if 'All' in c:
                                database1 = database1.copy()
                            else:

                                c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                b = [x for x in c_tuple] 
                                database1 = database1[database1['OCC_DOW'].isin(b)]

                            c = str(input.timerange())

                            if 'All' in c:
                                database1 = database1.copy()
                            else:

                                c_tuple = ast.literal_eval(c)  # Convert string to tuple
                                b = [x for x in c_tuple] 
                                database1 = database1[database1['Time Range'].isin(b)]



                            Meas = input.filter_worstDiv()
                            if Meas == "Collisions":
                                # Step 1: Count collisions per DIV
                                div_counts = database1['DIV'].value_counts().reset_index()

                                # Step 2: Rename columns for clarity
                                div_counts.columns = ['DIV', 'collision_count']

                                # Step 3: Get the top 5 DIVs as a DataFrame
                                top5_divs_df = div_counts.head(5)

                                
                                plt.figure(figsize=(4, 3))
                                plt.bar(top5_divs_df['DIV'], top5_divs_df['collision_count'], color='red')
                                plt.title('Worst Divisions by Number of Collisions', fontsize=8)
                                plt.xlabel('DIV', fontsize=8)
                                plt.ylabel('Number of Collisions',  fontsize=8)
                                plt.grid(axis='y', linestyle='--', alpha=0.7)
                                plt.xticks(rotation=0, fontsize=6)
                                plt.yticks(fontsize=8)
                                plt.tight_layout()
                            else:
                                # Step 1: Sum fatalities per DIV
                                fatalities_by_div = database1.groupby('DIV')['FATALITIES'].sum().reset_index()

                                # Step 2: Sort in descending order
                                fatalities_by_div = fatalities_by_div.sort_values(by='FATALITIES', ascending=False)

                                # Step 3: Get top 5 worst DIVs by fatalities
                                top5_fatal_divs = fatalities_by_div.head(5)

                                plt.figure(figsize=(4, 3))
                                plt.bar(top5_fatal_divs['DIV'], top5_fatal_divs['FATALITIES'], color='purple')
                                plt.title('Worst Divisions by Total Fatalities', fontsize=8)
                                plt.xlabel('DIV', fontsize=8)
                                plt.ylabel('Total Fatalities', fontsize=8)
                                plt.grid(axis='y', linestyle='--', alpha=0.7)
                                plt.xticks(rotation=0, fontsize=6)
                                plt.yticks(fontsize=8)
                                plt.tight_layout()

                    with ui.card(height='350px'):
                        
                        "kit"

                    with ui.card(height='350px'):
                        
                        "kit"
        with ui.nav_panel("Neighborhood-based Analysis"):
            "Panel C content"

