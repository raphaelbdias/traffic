""" MAIN development FLASK """
import io
import base64
import osmnx as ox
import networkx as nx
from flask import Flask, render_template, request, render_template_string
from calculations import create_geodataframe, osm_network
import matplotlib.pyplot as plt
import geopandas as gpd
import geopy
import folium
from folium.plugins import FastMarkerCluster
import geocoder
from folium import IFrame
from cars_static import get_traffic_info



# url = 'https://raw.githubusercontent.com/raphaelbdias/traffic/main/TrafficData.csv?token=GHSAT0AAAAAACEPSUZXJ36YCNTVOP725UUKZE5ZOCQ'
# records = requests.get(url).content

# df = pd.read_csv('TrafficData.csv')
# print(calculate_distance(df))



app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def display_image():
    API_KEY = "ryiGHGAMQ3KcmGg9hgNYkRODCxfAMeIL"
    if request.method == "POST":
        # Get the location input from the form
        city_name = request.form["city"]
        origin_name = request.form["origin"]
        destination_name = request.form["destination"]
        

        # Retrieve the street network graph for the city
        G = ox.graph_from_place(city_name, network_type="drive")
        # Impute edge (driving) speeds and calculate edge traversal times
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)


        def get_latlng(location):
            g = geocoder.osm(location, method='reverse')
            coordinates = g.latlng
            return coordinates

        # Get origin and destination coordinates
        origin_point = get_latlng(origin_name)
        destination_point = get_latlng(destination_name)
        print(origin_point, destination_point)

        # Find the closest graph nodes to origin and destination
        orig_node = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0])
        destination_node = ox.distance.nearest_nodes(
            G, destination_point[1], destination_point[0]
        )

        # Find the shortest path based on travel time
        route = nx.shortest_path(G, orig_node, destination_node, weight="travel_time")

        # Create a folium map centered around the origin
        m = folium.Map(location=[origin_point[0], origin_point[1]], zoom_start=12)

        # Add the route to the map
        route_coordinates = [(G.nodes[route[i]]["y"], G.nodes[route[i]]["x"]) for i in range(len(route))]
        folium.PolyLine(route_coordinates, color='blue', weight=2.5, opacity=1).add_to(m)

        # Add markers for the origin and destination
        folium.Marker(location=[origin_point[0], origin_point[1]], popup='Origin').add_to(m)
        folium.Marker(location=[destination_point[0], destination_point[1]], popup='Destination').add_to(m)

        # Add the route to the map
        route_coordinates = [(G.nodes[route[i]]["y"], G.nodes[route[i]]["x"]) for i in range(len(route))]
        folium.PolyLine(route_coordinates, color='blue', weight=2.5, opacity=1).add_to(m)

        # Iterate over the edges in the route
        for i in range(len(route)-1):
            u = route[i]
            v = route[i+1]

            # Get the coordinates of the edge's start and end nodes
            start_lat = G.nodes[u]["y"]
            start_lon = G.nodes[u]["x"]
            end_lat = G.nodes[v]["y"]
            end_lon = G.nodes[v]["x"]

            # Get traffic flow information for the edge
            traffic_info = get_traffic_info(API_KEY, start_lat, start_lon)
            if traffic_info is not None:
                # Extract relevant traffic data from the traffic_info
                current_speed = int(traffic_info['flowSegmentData']['currentSpeed'])
                free_flow_speed = int(traffic_info['flowSegmentData']['freeFlowSpeed'])
                print(current_speed,free_flow_speed)

                # Calculate the congestion factor
                congestion_factor = current_speed / free_flow_speed
                print(congestion_factor)

                # Choose a color based on the congestion factor
                if congestion_factor < 0.7:
                    color = 'red'
                elif congestion_factor < 0.3:
                    color = 'yellow'
                else:
                    color = 'green'

                # Add the edge with the corresponding color to the map
                folium.PolyLine([(start_lat, start_lon), (end_lat, end_lon)],
                                color=color, weight=2.5, opacity=1).add_to(m)

        # Add markers for the origin and destination
        folium.Marker(location=[origin_point[0], origin_point[1]], popup='Origin').add_to(m)
        folium.Marker(location=[destination_point[0], destination_point[1]], popup='Destination').add_to(m)

        return m._repr_html_()
    else:
        # Render the initial template with the form
        return render_template("index.html")


# @app.route("/test", methods=["GET", "POST"])
# def display_image_test():
#     if request.method == "POST":
#         # Process form data and generate the route
#         g = geocoder.ip('me')
#         print(g)
#         longitude, latitude = g.latlng
#         print(g.latlng)

#         # Reverse geocoding to get the location name
#         location = geocoder.osm([longitude, latitude], method='reverse')
#         print(location)
#         location_name = location.address
#         print(location_name)
        
#         city_name = location_name

#         # Retrieve the street network graph for the city
#         G = ox.graph_from_point(tuple((longitude, latitude)), network_type="drive")
#         # Impute edge (driving) speeds and calculate edge traversal times
#         G = ox.add_edge_speeds(G)
#         G = ox.add_edge_travel_times(G)

#         # Convert string address into geographical coordinates
#         def geocode_address(address, crs=4326):
#             geocode = gpd.tools.geocode(
#                 address, provider="nominatim", user_agent="drive time demo"
#             ).to_crs(crs)
#             return (geocode.iloc[0].geometry.y, geocode.iloc[0].geometry.x)

#         # Get origin and destination coordinates
#         origin_point = geocode_address(city_name)
#         destination_point = geocode_address(destination_name)

#         # Find the closest graph nodes to origin and destination
#         orig_node = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0])
#         destination_node = ox.distance.nearest_nodes(
#             G, destination_point[1], destination_point[0]
#         )

#         # Find the shortest path based on travel time
#         route = nx.shortest_path(G, orig_node, destination_node, weight="travel_time")

#         # Create a folium map centered around the origin
#         m = folium.Map(location=[origin_point[0], origin_point[1]], zoom_start=12)

#         # Add the route to the map
#         route_coordinates = [(G.nodes[route[i]]["y"], G.nodes[route[i]]["x"]) for i in range(len(route))]
#         folium.PolyLine(route_coordinates, color='blue', weight=2.5, opacity=1).add_to(m)

#         # Add markers for the origin and destination
#         folium.Marker(location=[origin_point[0], origin_point[1]], popup='Origin').add_to(m)
#         folium.Marker(location=[destination_point[0], destination_point[1]], popup='Destination').add_to(m)

#         # Generate the HTML for the form
#         form_html = """
#         <div id="form-container">
#             <form method="POST" action="/">
#                 <label for="origin">Origin:</label>
#                 <input type="text" id="origin" name="origin" required><br><br>
#                 <label for="destination">Destination:</label>
#                 <input type="text" id="destination" name="destination" required><br><br>
#                 <input type="submit" value="Submit">
#             </form>
#         </div>
#         """

#         # Render the template with the map and form HTML
#         return render_template_string(
#             """
#             <!DOCTYPE html>
#             <html>
#             <head>
#                 <title>Display Image</title>
#                 <style>
#                     #map-container {
#                         position: relative;
#                         width: 100%;
#                         height: 500px;
#                     }
#                     #form-container {
#                         position: absolute;
#                         top: 10px;
#                         left: 10px;
#                         background-color: white;
#                         padding: 10px;
#                     }
#                 </style>
#             </head>
#             <body>
#                 <div id="map-container">{{ map_html }}</div>
#             </body>
#             </html>
#             """,
#             map_html=m._repr_html_(),
#         )
#     else:

#         g = geocoder.ip('me')
#         print(g)
#         longitude, latitude = g.latlng
#         print(g.latlng)

#         # Reverse geocoding to get the location name
#         location = geocoder.osm([longitude, latitude], method='reverse')
#         print(location)
#         location_name = location.address
#         print(location_name)
        
#         city_name = location_name

#         # Retrieve the street network graph for the city
#         G = ox.graph_from_point(tuple((longitude, latitude)), network_type="drive")
#         # Impute edge (driving) speeds and calculate edge traversal times
#         G = ox.add_edge_speeds(G)
#         G = ox.add_edge_travel_times(G)

#         # Convert string address into geographical coordinates
#         def geocode_address(address, crs=4326):
#             geocode = gpd.tools.geocode(
#                 address, provider="nominatim", user_agent="drive time demo"
#             ).to_crs(crs)
#             return (geocode.iloc[0].geometry.y, geocode.iloc[0].geometry.x)

#         # Get origin and destination coordinates
#         origin_point = geocode_address(city_name)

#         # Create a folium map centered around the origin
#         m = folium.Map(location=[origin_point[0], origin_point[1]], zoom_start=12)
#         # Create a folium map centered around the user's location
#         m = folium.Map(location=[latitude, longitude], zoom_start=12)

#         # Generate the HTML for the form
#         form_html = """
#         <div id="form-container">
#             <form method="POST" action="/">
#                 <label for="origin">Origin:</label>
#                 <input type="text" id="origin" name="origin" required><br><br>
#                 <label for="destination">Destination:</label>
#                 <input type="text" id="destination" name="destination" required><br><br>
#                 <input type="submit" value="Submit">
#             </form>
#         </div>
#         """

#         # Render the template with the map and form HTML
#         return render_template_string(
#             """
#             <!DOCTYPE html>
#             <html>
#             <head>
#                 <title>Display Image</title>
#                 <style>
#                     #map-container {
#                         position: relative;
#                         width: 100%;
#                         height: 500px;
#                     }
#                     #form-container {
#                         position: absolute;
#                         top: 10px;
#                         left: 10px;
#                         background-color: white;
#                         padding: 10px;
#                     }
#                 </style>
#             </head>
#             <body>
#                 <div id="map-container">{{ map_html }}</div>
#             </body>
#             </html>
#             """,
#             map_html=m._repr_html_(),
#         )

if __name__ == "__main__":
    app.run(debug=True, port=8080)
