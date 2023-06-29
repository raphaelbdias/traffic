import pandas as pd
import math

def calculate_distance(df):
    distances = {}
    previous_x = {}
    previous_y = {}

    for _, record in df.iterrows():
        car_id = record['car_id']
        x = record['location_x']
        y = record['location_y']

        if car_id not in distances:
            distances[car_id] = 0
            previous_x[car_id] = None
            previous_y[car_id] = None

        if previous_x[car_id] is not None and previous_y[car_id] is not None:
            distance = math.sqrt((x - previous_x[car_id]) ** 2 + (y - previous_y[car_id]) ** 2)
            distances[car_id] += distance

        previous_x[car_id] = x
        previous_y[car_id] = y

    return distances