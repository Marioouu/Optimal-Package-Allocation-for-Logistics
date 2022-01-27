import random 
import pandas as pd
import numpy as np
import math

def generate_locs_two_region(num_rows):
    lat = [18.627160, 18.621160]
    lon = [73.810552, 73.860552]

    result = []

    for _ in range(num_rows):
        dec_lat = random.random()/100
        dec_lon = random.random()/100
        result.append((random.choice(lat) + dec_lat, random.choice(lon) + dec_lon))
    return result

def generate_locs(num_rows):
    lat = (18.627160 + 18.621160)/2
    lon = (73.810552 + 73.860552) / 2

    result = []

    for _ in range(num_rows):
        dec_lat = random.random()/100
        dec_lon = random.random()/100
        result.append((lat + dec_lat, lon + dec_lon))
    return result

def read_data():
    df_depots = pd.read_csv('./data/city_depots1.csv', header=None)
    df_drops = pd.read_csv('./data/city_drops1.csv', header=None)


    # drop_indices = np.random.choice(df_drops.index, 8714, replace=False)
    # depot_indices = np.random.choice(df_depots.index, 105, replace=False)
    # df_drops = df_drops.drop(drop_indices)
    # df_depots = df_depots.drop(depot_indices)


    # df_drops.to_csv('city_drops1.csv', header=False, index=False)
    # df_depots.to_csv('city_depots1.csv', header=False, index=False)

    depots = np.column_stack((df_depots[2], df_depots[1]))
    drops = np.column_stack((df_drops[2], df_drops[1]))
    return [depots, drops]
