from ortools.linear_solver import pywraplp
from geopy.distance import geodesic
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import random 
from vrp import *
from visualizer import *
from generator import *
from scipy.spatial.distance import cdist
from sklearn.metrics import pairwise_distances, pairwise

def initialize_cost(depot_locations, drop_locations):
    m = len(depot_locations)
    n = len(drop_locations)
    cost = pairwise.haversine_distances([[math.radians(_[0]), math.radians(_[1])] for _ in depot_locations] , [[math.radians(_[0]), math.radians(_[1])] for _ in drop_locations] ) * 6371
    return cost

def optimization(depot_locations, drop_locations, depot_capacity, calculate_vrp):

    num_depots = len(depot_locations)
    num_drops = len(drop_locations)

    # Maximum total of drop sizes for any depot
    # depot_capacity = np.random.randint(120, size=(num_depots))
    # depot_capacity = [2000, 2000, 2000, 3000, 3000]
    total_capacity = sum(depot_capacity)
    costs = initialize_cost(depot_locations, drop_locations)

    print(num_depots)
    print(num_drops)


    # Solver
    # Create the mip solver with the CBC backend.
    # Set to GUROBI for faster and more optimized results (Requires license)
    solver = pywraplp.Solver.CreateSolver('CBC')

    # Variables
    # x[i, j] is an array of 0-1 variables, which will be 1
    # if depot i is assigned to drop j.
    x = {}
    for depot in range(num_depots):
        for drop in range(num_drops):
            x[depot, drop] = solver.BoolVar(f'x[{depot},{drop}]')
    
    # Constraints
    # The total size of the drops each depot i takes on is at most depot_capacity[i].
    for depot in range(num_depots):
        solver.Add(
            solver.Sum([
                x[depot, drop] for drop in range(num_drops)
            ]) <= depot_capacity[depot])

    # Each drop is assigned to exactly one or none depot.
    for drop in range(num_drops):
        solver.Add(
            solver.Sum([x[depot, drop] for depot in range(num_depots)]) <= 1)

    print("Constraints setting done!")

    # Objective
    objective_terms = []
    for depot in range(num_depots):
        for drop in range(num_drops):
            objective_terms.append(costs[depot][drop] * x[depot, drop])
    
    for drop in range(num_drops):
        objective_terms.append(500 * (1 - solver.Sum([x[depot, drop] for depot in range(num_depots)])))

    print("Objective setting done!")
    solver.set_time_limit(10*1000)
    solver.Minimize(solver.Sum(objective_terms))

    # Solve
    print("Starting solver!")
    status = solver.Solve()
    print(status)
    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        plotter(depot_locations, drop_locations)
        print(f'Total cost = {solver.Objective().Value()}\n')

        nodes={}

        #--------PLOTS ALLOCATIONS--------------#

        optimization_plotter(depot_locations, drop_locations, x)
        if(calculate_vrp):
            plt.figure()
            plotter(depot_locations, drop_locations)

        for depot in range(num_depots):
            for drop in range(num_drops):
                if x[depot, drop].solution_value() > 0.5: 
                    if depot in nodes:
                        nodes[depot].append(drop)
                    else:
                        nodes[depot] = []
                        nodes[depot].append(drop)
                    
                    print(f'depot {depot} assigned to drop {drop}.' +
                          f' Cost: {costs[depot][drop]}')

            if(calculate_vrp):
                if depot in nodes:
                    vrpData = [depot_locations[depot]]
                    for depo_node in nodes[depot]:
                        vrpData.append(drop_locations[depo_node])
                vrp_calculator(vrpData)
    else:
        print('No solution found.')
