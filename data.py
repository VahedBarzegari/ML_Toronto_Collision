import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import zipfile

# Step 1: Load your CSV from ZIP
with zipfile.ZipFile("Traffic_Collisions_All.zip") as zipf:
    with zipf.open("Traffic_Collisions_All.csv") as file:
        df = pd.read_csv(file)

# Step 2: Preprocess the DataFrame
df['FATALITIES'] = df['FATALITIES'].fillna(0).astype(int)
df.drop(['DIVISION', 'HOOD_158', 'NEIGHBOURHOOD_158'], axis=1, inplace=True, errors='ignore')

# Step 3: Convert df to a GeoDataFrame with points
geometry = [Point(xy) for xy in zip(df['LONG_WGS84'], df['LAT_WGS84'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# Step 4: Load DIV_Boundaries.geojson and join for DIV
geo_div = gpd.read_file('DIV_Boundaries.geojson')  # Must have a 'DIV' column
gdf = gpd.sjoin(gdf, geo_div[['DIV', 'geometry']], how='left', predicate='within')
gdf.drop(columns=['index_right'], inplace=True)

# Step 5: Load toronto_crs84.geojson and join for NEIGHBOURHOOD_158
geo_hood = gpd.read_file('toronto_crs84.geojson')  # Must have 'AREA_NAME'
geo_hood.rename(columns={'AREA_NAME': 'NEIGHBOURHOOD_158'}, inplace=True)
gdf = gpd.sjoin(gdf, geo_hood[['NEIGHBOURHOOD_158', 'geometry']], how='left', predicate='within')
gdf.drop(columns=['index_right'], inplace=True)

# Optional: Drop geometry if not needed
gdf.drop(columns='geometry', inplace=True)

# Resulting DataFrame
df = pd.DataFrame(gdf)

columns_to_convert = ['INJURY_COLLISIONS', 'FTR_COLLISIONS', 'PD_COLLISIONS']
df[columns_to_convert] = df[columns_to_convert].applymap(lambda x: 1 if x == 'YES' else 0)

database = df.copy()