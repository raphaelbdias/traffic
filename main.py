import requests
import pandas as pd
# import io
from calculations import calculate_distance

# url = 'https://raw.githubusercontent.com/raphaelbdias/traffic/main/TrafficData.csv?token=GHSAT0AAAAAACEPSUZXJ36YCNTVOP725UUKZE5ZOCQ'
# records = requests.get(url).content

df = pd.read_csv('TrafficData.csv')
print(calculate_distance(df))