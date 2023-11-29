from Structure import *

# Demands: 3
# Index, Origin, Destination, Volume


def Reading(file_name):
        
    data = open(f"{file_name}", "r")
    demands_amount = int(data.readline().split(":")[1])
    data.readline()
    demands = []
    for d in range(demands_amount):
        each_demand = []
        for i in data.readline().split(','):
            each_demand.append(int(i.strip()))
        demands.append(Demand(each_demand[0], each_demand[1], each_demand[2], each_demand[3]))
        
    data.readline()
    stations_amount = int(data.readline().split(":")[1])
    data.readline()
    stations = []
    for s in range(stations_amount):
        a = [int(i.strip()) for i in data.readline().split(',')]
        stations.append(Station(a[0], a[1], a[2]))
        
    data.readline()
    blocks_amount = int(data.readline().split(":")[1])
    data.readline()
    blocks = []
    for b in range(blocks_amount):
        a = [int(i.strip()) for i in data.readline().split(',')]
        blocks.append(Block(a[0], a[1], a[2], a[3]))
        
    return demands_amount, demands, stations_amount, stations, blocks_amount, blocks