''' CALCULATION FILES '''
import io
import base64
import math
import geopandas as gpd
from shapely.geometry import LineString, Point
import osmnx  as ox
import networkx as nx
import matplotlib.pyplot as plt


def calculate_distance(geo_df):

    ''' calculates the euclidean distance '''
    distances = {}
    previous_x = {}
    previous_y = {}

    for _, record in geo_df.iterrows():
        car_id = record["car_id"]
        coor_x = record["location_x"]
        coor_y = record["location_y"]

        if car_id not in distances:
            distances[car_id] = 0
            previous_x[car_id] = None
            previous_y[car_id] = None

        if previous_x[car_id] is not None and previous_y[car_id] is not None:
            distance = math.sqrt(
                (coor_x - previous_x[car_id]) ** 2 + (coor_y - previous_y[car_id]) ** 2
            )
            distances[car_id] += distance

        previous_x[car_id] = coor_x
        previous_y[car_id] = coor_y

    return distances


def create_geodataframe(name, longitude, latitude):

    ''' create origin/destination gdf '''

    gdf = gpd.GeoDataFrame(columns=['name', 'geometry'], crs=4326, geometry='geometry')
    gdf.at[0, 'geometry'] = Point(longitude, latitude)
    gdf.at[0, 'name'] = name
    return gdf


def osm_network(origin, destination, network='drive'):
    # creating a boundary for fetching OSM data
    combined = origin._append(destination)
    convex = combined.unary_union.convex_hull
    graph_extent = convex.buffer(0.02)

    
    # fetching graph
    graph = ox.graph_from_polygon(graph_extent, network_type=network)
    
    # Get the edges/network as GeoDataFrame
    edges = ox.graph_to_gdfs(graph, nodes=False)
    
    # Convert the GeoDataFrame to an image
    image = edges.plot(figsize=(10, 10), edgecolor="black", linewidth=0.5)

    # Save the image to a BytesIO object
    buffer = io.BytesIO()
    image.figure.savefig(buffer, format="png")
    buffer.seek(0)
    # Encode the image as base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    # Display or return the base64 encoded image
    return image_base64


# def shortest_path(origin, destination, network = 'drive'):
    # ''' 
    # origin and destination <GeoDataFrame> crs 4326, network <str> drive, bike, walk
    # RETURN shortest path <GeoDataFrame>
    
    # '''
    # # creating a frame for fetching OSM data
    # combined = origin.append(destination)
    
    # convex = combined.unary_union.convex_hull
    
    # graph_extent = convex.buffer(0.02)
    
    # # fetching graph
    # graph = ox.graph_from_polygon(graph_extent, network_type= network)
    
    # # Reproject the graph
    # graph_proj = ox.project_graph(graph)
    
    # # Get the edges as GeoDataFrame
    # edges = ox.graph_to_gdfs(graph_proj, nodes=False)
    
    # # Get CRS info UTM
    # CRS = edges.crs
    
    # # Reproject all data
    # origin_proj = origin.to_crs(crs=CRS)
    # destination_proj = destination.to_crs(crs=CRS)
    
    # # routes of shortest path
    # routes = gpd.GeoDataFrame()
    
    # # Get nodes from the graph
    # nodes = ox.graph_to_gdfs(graph_proj, edges=False)
    
    # # Iterate over origins and destinations
    # for oidx, orig in origin_proj.iterrows():
    
    # # Find closest node from the graph → point = (latitude, longitude)
    # # closest_origin_node = ox.get_nearest_node(G=graph_proj, point=(orig.geometry.y, orig.geometry.x), method=’euclidean’)
    
    # # Iterate over targets
    #     for tidx, target in destination_proj.iterrows():
    #     # Find closest node from the graph → point = (latitude, longitude)
    #     closest_target_node = ox.get_nearest_node(graph_proj, point=(target.geometry.y, target.geometry.x), method=’euclidean’)
    #     # Check if origin and target nodes are the same → if they are → skip
    #     if closest_origin_node == closest_target_node:
    #         print(“Same origin and destination node. Skipping ..”)
    #         continue
    
    #     # Find the shortest path between the points
    #     route = nx.shortest_path(graph_proj, 
    #                                 source=closest_origin_node, 
    #                                 target=closest_target_node, weight=’length’)
    
    #     # Extract the nodes of the route
    #     route_nodes = nodes.loc[route]
    
    #     # Create a LineString out of the route
    #     path = LineString(list(route_nodes.geometry.values))
    
    #     # Append the result into the GeoDataFrame
    #     routes = routes.append([[path]], ignore_index=True)
    # # Add a column name
    # routes.columns = [‘geometry’]
    
    # # Set coordinate reference system
    # routes.crs = nodes.crs
    # # Set geometry
    # routes = routes.set_geometry(‘geometry’)
    
    # return routes