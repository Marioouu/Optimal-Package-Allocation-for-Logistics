from ortools.linear_solver import pywraplp
from geopy.distance import geodesic
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import random 
import math
from scipy.spatial.distance import cdist
from sklearn.metrics import pairwise_distances, pairwise
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def getDistance(p1, p2):
    return geodesic(p1, p2).km

def create_data_model(vrpData):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = []

    # for i in vrpData:
    #     dm = []
    #     for j in vrpData:
    #         dm.append(math.ceil(geodesic(i, j).km * 100))
    #     data['distance_matrix'].append(dm)

    # data['distance_matrix'] = cdist(vrpData, vrpData, getDistance)
    # data['distance_matrix'] = pairwise_distances(vrpData, vrpData, getDistance)

    vrpData = [[math.radians(_[0]), math.radians(_[1])] for _ in vrpData]
    data['distance_matrix']= np.ceil(pairwise.haversine_distances(vrpData) * 637100)

    print("Calculated distance matrix!")
    
    num_drops = len(vrpData) - 1
    num_vehicles = math.ceil(num_drops / 5)
    
    if num_vehicles == 0:
        num_vehicles = 1
    data['demands'] = np.ones(num_drops + 1)
    data['demands'][0] = 0
    data['vehicle_capacities'] = 15 * np.ones(num_vehicles)
    data['num_vehicles'] = num_vehicles
    data['depot'] = 0
    data['num_drops'] = num_drops
    print([num_drops, sum(data['vehicle_capacities'])])
    return data


def print_solution(data, manager, routing, solution, vrpData):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        if data['num_drops'] <= vehicle_id:
            continue
        index = routing.Start(vehicle_id)
        # plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0

        x_d = []
        y_d = []
        
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            x_d.append(vrpData[node_index][0])
            y_d.append(vrpData[node_index][1])

            route_load += data['demands'][node_index]
            # plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        x_d.append(x_d[0])
        y_d.append(y_d[0])
        plt.plot(x_d, y_d)
        # plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
        #                                          route_load)
        # plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        # plan_output += 'Load of the route: {}\n'.format(route_load)
        # print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))


def vrp_calculator(vrpData):
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model(vrpData)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')
    penalty = 100
    for node in range(1, len(data['distance_matrix'])):
        routing.AddDisjunction([manager.NodeToIndex(node)], penalty)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        # routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        # routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC)
        routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING)
    search_parameters.time_limit.FromSeconds(5)
    # search_parameters.time_limit.seconds = 5

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    print(routing.status())
    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution, vrpData)
    else:
        print("No solution")