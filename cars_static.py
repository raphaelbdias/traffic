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

# Example usage
csv_file = 'streetdata_sudbury.csv'
highway_name = 'Highway 144'
total_length = find_highway_length(csv_file, highway_name)
print(f"The total length of {highway_name} is: {total_length} units")