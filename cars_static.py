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

def find_highway_length(csv_file, highway_name):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        total_length = 0
        
        for row in reader:
            if row['name'] == highway_name:
                length = float(row['length'])
                total_length += length
        
        return total_length

# Random point
csv_file = 'TrafficData.csv'
# Example usage
csv_file = 'streetdata_sudbury.csv'
highway_name = 'Highway 144'
total_length = find_highway_length(csv_file, highway_name)
print(f"The total length of {highway_name} is: {total_length} units")

import csv
import random

def get_random_point_from_geometry(csv_file):
    # Step 1: Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        geometries = list(reader)

    if not geometries:
        return None

    # Step 3: Generate a random index
    random_index = random.randint(0, len(geometries) - 1)

    # Step 4: Retrieve the geometry
    random_geometry = geometries[random_index]

    # Step 5: Get the random point
    random_point = random_geometry['geometry']

    return random_point

# Usage
random_point = get_random_point_from_geometry('geometry_data.csv')
print(random_point)