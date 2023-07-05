''' this is for testing solutions '''

# from calculations import create_geodataframe, osm_network

# # Kamppi shopping center as Origin
# origin = create_geodataframe('Kamppi', 24.933260, 60.169111)

# # Physicum as Destination
# destination = create_geodataframe('Physicum', 24.962608, 60.205301)

# osm_network(origin, destination)


import geocoder

g = geocoder.ip('me')
latitude, longitude = g.latlng

# Reverse geocoding to get the location name
location = geocoder.osm([latitude, longitude], method='reverse')
location_name = location.address

print(f"Latitude: {latitude}, Longitude: {longitude}")
print(f"Location Name: {location_name}")