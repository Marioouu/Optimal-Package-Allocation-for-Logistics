import matplotlib.pyplot as plt

def plotter(depot_locations, drop_locations, solver):
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

    
    plt.scatter(x=x_depot, y=y_depot, color='r', s=100)
    plt.scatter(x=x_drop, y=y_drop, color='b')