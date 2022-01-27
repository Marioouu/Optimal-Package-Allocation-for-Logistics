from generator import *
from optimization import * 
import greedy3 as g3
import greedy1 as g1
import matplotlib.pyplot as plt
from visualizer import *

def main():
    # drop_locations = generate_locs(20)
    # depot_locations = generate_locs(4)
    [depot_locations, drop_locations] = read_data()
    # depot_capacity = np.random.randint(10, size=(len(depot_locations)))
    depot_capacity = np.ones(len(depot_locations)) * (len(drop_locations) / len(depot_locations) * 1.5)

    plt.xlabel('Latitude')
    plt.ylabel('Longitude')

    #------Runs the MIP solver----------#
    #------Set True if VRP needs to be calculated-----#
    optimization(depot_locations, drop_locations, depot_capacity, False)
    #-------Runs the Greedy Solver-------#
    plt.figure()
    g1.greedy(depot_locations, drop_locations, depot_capacity)


    # plotter(depot_locations, drop_locations)
    plt.show()

if __name__ == '__main__':
    main()