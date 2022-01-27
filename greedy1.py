from generator import *
from geopy.distance import geodesic
import numpy as np
from visualizer import * 
from matplotlib.pyplot import cm

def initialize_cost(depot_locations, drop_locations, capacity):
    m = len(depot_locations)
    n = len(drop_locations)
    drops = [Drop() for i in range(n)]
    depots = []

    for depo in range(m):
        depots.append(Depot(depo, capacity[depo]))
    
    for drop in range(n):
        for depot in range(m):
            drops[drop].addDepot(depot, geodesic(depot_locations[depot], drop_locations[drop]).km )
        drops[drop].sort_distances()
    # drops.sort(key=lambda x: x.depot_distances[0][0], reverse=False)
    return [drops, depots]

class Drop():
    # assignedDepot = None
    def __init__(self):
        self.depot_distances = []
        self.current_neighbour = 0
    
    def addDepot(self, depotIndex, depotDistance):
        self.depot_distances.append([depotDistance, depotIndex])

    def sort_distances(self):
        self.depot_distances.sort()
    

class Depot():
    def __init__(self, index, capacity):
        self.index = index
        self.capacity = capacity
        self.filled = 0
        self.drops = set()
        
    def addDrop(self, dropIndex):
        if dropIndex not in self.drops:
            self.drops.add(dropIndex)
            self.filled += 1

    def removeDrop(self, dropIndex):
        if dropIndex in self.drops:
            self.drops.remove(dropIndex) 
            self.filled -= 1

    def isSpace(self):
        return self.capacity > self.filled 

def greedy(depot_locations, drop_locations, depot_capacity):

    num_depots = len(depot_locations)
    num_drops = len(drop_locations)

    # Maximum total of drop sizes for any depot
    # depot_capacity = np.random.randint(20, size=(num_depots))
    # depot_capacity = [2000, 2000, 2000, 3000, 3000]
    total_capacity = sum(depot_capacity)
    [drops, depots] = initialize_cost(depot_locations, drop_locations, depot_capacity)

    # print(num_depots)
    # print(num_drops)

    for i in range(len(drops)):
        # drop = drops[i]
        current_nearest_neighbour = drops[i].depot_distances[drops[i].current_neighbour][1]
        # depot = depots[current_nearest_neighbour]
        depots[current_nearest_neighbour].addDrop(i)
        # print("assign drop {%d} to depot {%d}"%(i, current_nearest_neighbour))
        # plt.plot([depot_locations[current_nearest_neighbour][0], drop_locations[i][0]], [depot_locations[current_nearest_neighbour][1], drop_locations[i][1]])
    
    for q in range(len(depots)):
        for i in range(len(depots)):
            cost_list = []
            depot = depots[i]

            # print("checking dept {%d}: isSpace: {%d}"%(i, depots[i].isSpace()))
            if depots[i].filled <= depots[i].capacity:
                continue

            for drop_index in depot.drops:
                drop = drops[drop_index]
                drop_current_neighbour = drop.current_neighbour+1

                while drop_current_neighbour < len(drop.depot_distances) and (not depots[drop.depot_distances[drop_current_neighbour][1]].isSpace()):
                    # print("checking: depot {%d} | drop {%d} | neighbour {%d} | isSpace {%d}"%(i, drop_index, drop.depot_distances[drop_current_neighbour][1], depots[drop.depot_distances[drop_current_neighbour][1]].isSpace()))
                    drop_current_neighbour += 1

                if drop_current_neighbour == len(drop.depot_distances):
                    continue

                [neighbour_distance, neighbour_index] = drop.depot_distances[drop_current_neighbour]
                cost_list.append([neighbour_distance - drop.depot_distances[drop.current_neighbour][0], drop_index, drop_current_neighbour])
            
            cost_list.sort()
            number_transfers = depot.filled - depot.capacity
            # print("number transfer: {%d}"%(number_transfers))
            cost_list_index = 0
            count = 0

            while cost_list_index < len(cost_list) and count < number_transfers:
                [cost_increase, drop_index, next_neighbour] = cost_list[cost_list_index]
                if depots[drop.depot_distances[next_neighbour][1]].isSpace():
                    drops[drop_index].current_neighbour = next_neighbour
                    depots[i].removeDrop(drop_index)
                    depots[drop.depot_distances[next_neighbour][1]].addDrop(drop_index)
                    # print("transfer drop {%d} from depot {%d} to depot {%d}"%(drop_index, i, drop.depot_distances[next_neighbour][1]))
                    count += 1
                cost_list_index += 1

    cost = 0
    color = cm.Dark2(np.linspace(0, 1, 100))

    for i in range(len(depots)):
        depot = depots[i]
        c = random.choice(color)
        for j in depot.drops:
            plt.plot([depot_locations[i][0], drop_locations[j][0]], [depot_locations[i][1], drop_locations[j][1]], c = c, alpha=0.7, zorder=1)
            cost += geodesic([depot_locations[i][0], depot_locations[i][1]], [drop_locations[j][0], drop_locations[j][1]]).km

            

    plotter(depot_locations, drop_locations)
    # for depot in depots:
    #     print(depot.capacity - depot.filled)
    print("greedy cost:{%d}" %(cost))
    

