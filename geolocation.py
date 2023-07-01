import osmnx as ox
import geopandas as gpd
import sqlite3
import pandas as pd

def import_street_data_to_sqlite(place_name):
    # Get the street network for the specified place
    graph = ox.graph_from_place(place_name, network_type='drive')

    # Convert the graph to a GeoDataFrame
    gdf = ox.graph_to_gdfs(graph, nodes=False, edges=True)

    # Check the available columns in the GeoDataFrame
    return gdf

    # # Extract the necessary columns from the GeoDataFrame
    # edges_df = gdf[['osmid', 'name', 'highway', 'length', 'geometry']].copy()
    # nodes_df = gdf[['osmid', 'geometry']].copy()

    # # Clean the GeoDataFrame by removing rows with missing or invalid geometry
    # edges_df = edges_df.dropna(subset=['geometry'])
    # edges_df = edges_df[edges_df['geometry'].is_valid]

    # # Convert LineString objects to WKT format
    # edges_df['geometry'] = edges_df['geometry'].apply(lambda line: line.wkt)

    # # Create a SQLite connection
    # conn = sqlite3.connect(db_name)

    # # Import the extracted data into SQLite tables
    # edges_df.to_sql('edges', conn, if_exists='replace', index=False)
    # nodes_df.to_sql('nodes', conn, if_exists='replace', index=False)

    # # Close the SQLite connection
    # conn.close()

# Example usage
place_name = "Greater Sudbury, ON, Canada"
db_name = "street_data.db"

streetdata = import_street_data_to_sqlite(place_name)

# save the data to csv, turn function off after 1st save
# streetdata.to_csv('/workspaces/traffic/streetdata_sudbury.csv')

print(streetdata)