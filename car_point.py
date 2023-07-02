import pandas as pd
from shapely.geometry import Point, LineString
import geopandas as gpd

csv_data = pd.read_csv('TrafficData.csv')

csv_data['geometry'] = csv_data.apply(lambda row: Point(row['location_x'], row['location_y']), axis=1)

gdf_csv = gpd.GeoDataFrame(csv_data, geometry='geometry')

# Load the other CSV data into a pandas DataFrame
intersect = pd.read_csv('streetdata_sudbury.csv')

# Convert the other CSV coordinates into Shapely LineString geometries
intersect['geometry'] = intersect.apply(lambda row: LineString([(row['start_x'], row['start_y']), (row['end_x'], row['end_y'])]), axis=1)

# Convert the pandas DataFrame to a GeoPandas DataFrame
gdf_inter = gpd.GeoDataFrame(intersect, geometry='geometry')

# Perform a spatial join to find the matching LineString geometries for the points in gdf_csv
joined_data = gpd.sjoin(gdf_csv, gdf_inter, how='inner', op='intersects')

