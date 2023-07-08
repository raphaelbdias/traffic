# program for getting random cars within the geometry line string
"""
suggestions
    - undertsand 'lists', 'geometry' and 'sets'
    - important packages pandas, csv, geopandas

logic flow:
    - take input from csv file, define the geometry **kwarg as 'geometry' column
    - index "geometry" column [contains the LINSTRINGs]
    - randomly chooce a point for each each car in "TrafficData"
    
"""
import csv
import requests
import xmltodict


def find_highway_length(csv_file, highway_name):
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        total_length = 0

        for row in reader:
            if row["name"] == highway_name:
                length = float(row["length"])
                total_length += length

        return total_length


# Random point
csv_file = "TrafficData.csv"
# Example usage
csv_file = "streetdata_sudbury.csv"
highway_name = "Highway 144"
total_length = find_highway_length(csv_file, highway_name)
print(f"The total length of {highway_name} is: {total_length} units")

import csv
import random


def get_random_point_from_geometry(csv_file):
    # Step 1: Read the CSV file
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        geometries = list(reader)

    if not geometries:
        return None

    # Step 3: Generate a random index
    random_index = random.randint(0, len(geometries) - 1)

    # Step 4: Retrieve the geometry
    random_geometry = geometries[random_index]

    # Step 5: Get the random point
    random_point = random_geometry["geometry"]

    return random_point

def get_traffic_info(api_key, lat, lon):
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/xml?key={api_key}&point={lat},{lon}"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Process the response data here
        traffic_data = response.text
        # Return or further process the traffic_data as per your requirement
        data_dict = xmltodict.parse(traffic_data)
        return data_dict
    else:
        # Handle error cases here
        print("Error:", response.status_code)
        return None
