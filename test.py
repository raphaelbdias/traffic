''' this is for testing solutions '''

from calculations import create_geodataframe, osm_network

# Kamppi shopping center as Origin
origin = create_geodataframe('Kamppi', 24.933260, 60.169111)

# Physicum as Destination
destination = create_geodataframe('Physicum', 24.962608, 60.205301)

osm_network(origin, destination)