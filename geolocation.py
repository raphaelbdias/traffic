"""looks for the streets using OpenStreetMaps"""

import osmnx as ox

def import_street_data(place_name):

    """Get the street network for the specified place"""

    graph = ox.graph_from_place(place_name, network_type='drive')

    # Convert the graph to a GeoDataFrame
    gdf = ox.graph_to_gdfs(graph, nodes=False, edges=True)

    # Check the available columns in the GeoDataFrame
    return gdf

"""
    Example usage
    PLACE_NAME = "Greater Sudbury, ON, Canada"

    streetdata = import_street_data(PLACE_NAME)

    # save the data to csv, turn function off after 1st save
    # import pandas as pd
    # streetdata.to_csv('/workspaces/traffic/streetdata_sudbury.csv')

    print(streetdata, flush=False)
"""