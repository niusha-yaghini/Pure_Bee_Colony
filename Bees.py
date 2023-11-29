import numpy as np

class Bee:
    # each bee is equal to a valid solution, that has the body(data = array answer), and its fitness
    
    def __init__(self, demands, blocks):
                
        self.data = [[0 for i in range(len(blocks))] for j in range(len(demands))]
        self.fitness = None
        self.improvement_try = 0
        self.feasiblity = None

def _calculating_fitness(bee, blocks, demands):
    # fitness = the sum of all volumes of each demand_solution in our bee
    
    fitness = 0
    for demand_solution in range(len(bee.data)):
        for b in range(len(blocks)):
            if(bee.data[demand_solution][b]==1):
                fitness += demands[demand_solution].volume * blocks[b].cost
    bee.fitness = (fitness)*-1            
        