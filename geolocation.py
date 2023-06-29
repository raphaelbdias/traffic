import osmnx as ox
import geopandas as gpd
import sqlite3
import pandas as pd

def import_street_data_to_sqlite(place_name, db_name):
    # Get the street network for the specified place
    graph = ox.graph_from_place(place_name, network_type='all')

    # Convert the graph to a GeoDataFrame
    gdf = ox.graph_to_gdfs(graph, nodes=False, edges=True)

    # Check the column names in the GeoDataFrame
    print(gdf.columns)

    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Import Nodes Data from GeoDataFrame to SQLite
    nodes_df = gdf[['osmid', 'geometry']].copy()
    nodes_df['osmid'] = nodes_df['osmid'].astype(str)  # Convert osmid to string type
    nodes_df.to_sql('nodes', conn, if_exists='replace', index=False)

    # Import Edges Data from GeoDataFrame to SQLite
    edges_df = gdf[['osmid', 'u', 'v']].copy()
    edges_df['osmid'] = edges_df['osmid'].astype(str)  # Convert osmid to string type
    edges_df.to_sql('edges', conn, if_exists='replace', index=False)

    # Close the database connection
    conn.close()

    print("Street data imported successfully to SQLite database.")

# Specify the name that is used to search for the data
place_name = "Edgewood, Washington, D.C., USA"

# Specify the name of the SQLite database
db_name = "your_database.db"

# Call the function to import street data
import_street_data_to_sqlite(place_name, db_name)
