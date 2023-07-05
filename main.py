""" MAIN development FLASK """
import io
import base64
import osmnx as ox
import networkx as nx
from flask import Flask, render_template, request
from calculations import create_geodataframe, osm_network
import matplotlib.pyplot as plt
import geopandas as gpd
import geopy
import folium
from folium.plugins import FastMarkerCluster


# url = 'https://raw.githubusercontent.com/raphaelbdias/traffic/main/TrafficData.csv?token=GHSAT0AAAAAACEPSUZXJ36YCNTVOP725UUKZE5ZOCQ'
# records = requests.get(url).content

# df = pd.read_csv('TrafficData.csv')
# print(calculate_distance(df))

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def display_image():
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

        # Convert string address into geographical coordinates
        def geocode_address(address, crs=4326):
            geocode = gpd.tools.geocode(
                address, provider="nominatim", user_agent="drive time demo"
            ).to_crs(crs)
            return (geocode.iloc[0].geometry.y, geocode.iloc[0].geometry.x)

        # Get origin and destination coordinates
        origin_point = geocode_address(origin_name)
        destination_point = geocode_address(destination_name)

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

        # Display the map
        return m._repr_html_()
    else:
        # Render the initial template with the form
        return render_template("index.html")


@app.route("/points")
def two_points():
    # Kamppi shopping center as Origin
    origin = create_geodataframe("Kamppi", 24.933260, 60.169111)

    # Physicum as Destination
    destination = create_geodataframe("Physicum", 24.962608, 60.205301)

    combined = origin._append(destination)
    convex = combined.unary_union.convex_hull
    graph_extent = convex.buffer(0.02)

    # fetching graph
    graph = ox.graph_from_polygon(graph_extent, network_type="drive")

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

    image_base64 = osm_network(origin, destination)

    return render_template("two_points.html", image_base64=image_base64)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
