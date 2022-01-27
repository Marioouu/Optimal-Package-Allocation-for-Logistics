import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import random

def plotter(depot_locations, drop_locations):
    x_depot = []
    y_depot = []
    x_drop = []
    y_drop = []

    for depot in depot_locations:
        x_depot.append(depot[0])
        y_depot.append(depot[1])
    for drop in drop_locations:
        x_drop.append(drop[0])
        y_drop.append(drop[1])   

    
    plt.scatter(x=x_depot, y=y_depot, color='r', s=100, zorder=2, label='Service Centers')
    plt.scatter(x=x_drop, y=y_drop, color='b', zorder=0, alpha = 0.7, label='Drops')
    plt.legend()

def optimization_plotter(depot_locations, drop_locations, x):
    d={}
    color = cm.Dark2(np.linspace(0, 1, 100))

    for depot in range(len(depot_locations)):
        for drop in range(len(drop_locations)):

            if x[depot, drop].solution_value() > 0.5:
                if depot in d:
                        c = d[depot]
                else:
                    c = random.choice(color)
                    d[depot] = c
                plt.plot([depot_locations[depot][0], drop_locations[drop][0]], [depot_locations[depot][1], drop_locations[drop][1]], c = c, alpha=0.7, zorder=1)