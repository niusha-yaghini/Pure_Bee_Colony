import numpy as np
import Bees
import random
import copy
from Structure import *


class ABC_algorithm():
    # artificial bee colony algorithm 
    
    def __init__(self, Demands_amount, Demands, Stations_amount, Stations, Blocks_amount, Blocks, Employed_bees_num, Onlooker_bees_num, Max_improvement_try, Pc, Pm, K_Tournomet_Percent, Percedure_Type):
        self.demands_amount = Demands_amount
        self.demands = Demands
        self.stations_amount = Stations_amount
        self.stations = Stations
        self.blocks_amount = Blocks_amount
        self.blocks = Blocks
        self.employed_bees_num = Employed_bees_num
        self.onlooker_bees_num = Onlooker_bees_num
        self.max_improvement_try = Max_improvement_try
        self.crossover_probbility = Pc
        self.mutation_probblity = Pm/self.demands_amount
        self.percedure_type = Percedure_Type
        self.k_tournoment = int(K_Tournomet_Percent*self.employed_bees_num)
          

    def employed_bees(self, population):
        # making initial random answers (equal to amount of employed bees number)
        # do the improvement-try once on each of them
        # return the made answers
        
        if(len(population) == 0):
            for i in range(self.employed_bees_num):
                bee = self._making_bee()
                population.append(bee)
            
        # we try for improvement one time for each bee, if change happens we add one to improvement-try property of that bee
        for bee in population:
            change_flag = self._try_for_improvement(population, bee)
            if(change_flag): 
                bee.improvement_try = 0
            else: 
                bee.improvement_try += 1
                    
    def _making_bee(self):
        # each bee is a (amount of demands * amount of blocks) matrix
        
        bee = Bees.Bee(self.demands, self.blocks)

        data = []
        for demand in self.demands:
            demand_answer = self._make_demand_answer(demand)
            data.append(demand_answer)
            
        bee.data = data
        return bee
                
    def _make_demand_answer(self, demand):
        data = [0 for i in range(self.blocks_amount)]
        destination_flag = False

        # finding the first cell
        choosing_options = []
        for b_indx in range(self.blocks_amount):
            if ((demand.origin == self.blocks[b_indx].origin) and 
                    (demand.destination >= self.blocks[b_indx].destination)):
                choosing_options.append(b_indx)
        choosed_index = random.choice(choosing_options)
        data[choosed_index] = 1
        
        if(demand.destination == self.blocks[choosed_index].destination):
            destination_flag = True
        
        while(destination_flag == False):
            choosing_options = []
            for b_indx in range(self.blocks_amount):
                if ((self.blocks[choosed_index].destination == self.blocks[b_indx].origin) and 
                        (demand.destination >= self.blocks[b_indx].destination)):
                    choosing_options.append(b_indx)
                    
            if(len(choosing_options)==0):
                print("we are in trouble!!! in (make_demand_answer)")  
     
            choosed_index = random.choice(choosing_options)
            data[choosed_index] = 1
            
            if(demand.destination == self.blocks[choosed_index].destination):
                destination_flag = True
        
        return data              

    def _validality_check(self, bee):
        
        feasiblity_flag = True

        block_limits_check = [0 for i in range(self.stations_amount)]
        vagon_limits_check = [0 for i in range(self.stations_amount)]
        
        checked_blocks = [0 for i in range(self.blocks_amount)]

        for demand_solution in range(len(bee.data)):
            for b in range(self.blocks_amount):
                if(feasiblity_flag):
                    if (bee.data[demand_solution][b]==1):
                        o = self.blocks[b].origin
                        d = self.blocks[b].destination
                        if(checked_blocks[b]!=1):
                            checked_blocks[b] = 1
                            block_limits_check[o] += 1
                        vagon_limits_check[d] += self.demands[demand_solution].volume
                        if(block_limits_check[o]>self.stations[o].block_capacity):
                            feasiblity_flag = False
                        if(vagon_limits_check[d]>self.stations[d].vagon_capacity):
                            feasiblity_flag = False
        bee.feasiblity = feasiblity_flag
        return feasiblity_flag
                                    
    def onlooker_bees(self, population):
        # by rolette wheel precedure we do "onlooker_bees_num" times cross_over and mutation,
        # on solution that employed bees have made
                
        for bee in population:
            if(bee.fitness == None):
                Bees._calculating_fitness(bee, self.blocks, self.demands)
        
        sum_of_fitnesses = sum([bee.fitness for bee in population])
        
        for i in range(self.onlooker_bees_num):

            if(self.percedure_type == "Roulette Wheel"):
                # selecting the bee by roulette wheel
                bee = self._roulette_wheel(population, sum_of_fitnesses)
            elif(self.percedure_type == "Tournoment"):            
                # sele a bee by tournoment procedure
                bee = self._tournoment(population)
            
            # we try for improvement one time for each bee, if change happens we add one to improvement-try property of that bee
            change_flag = self._try_for_improvement(population, bee)
            if(change_flag): 
                bee.improvement_try = 0
            else: 
                bee.improvement_try += 1
                                                        
    def scout_bees(self, population):
        delete_bees = []
        new_bees = []
        for bee in population:
            if(bee.improvement_try >= self.max_improvement_try):
                delete_bees.append(bee)
                new_bees.append(self._making_bee())
        for i in range(len(delete_bees)):
            population.remove(delete_bees[i])
            population.append(new_bees[i])
                    
    def _try_for_improvement(self, population, bee):
        # we do the cross over and mutation here
        # we also return that if the process made any changes or not
        
        change_flag = False
        new_bee = copy.deepcopy(bee)
        
        # doing the cross over on selected bee and a neighbor (that will be handled in _cross_over)
        self._cross_over_one_point(population, new_bee)
        
        # doing the mutation on selected bee
        self._mutation(new_bee) 

        validality_flag_current_bee = self._validality_check(bee)
        validality_flag_new_bee = self._validality_check(new_bee)
        
        if(validality_flag_current_bee == False):
            # we need to set the new feasiblity and the new fitness
            
            bee.data = new_bee.data
            bee.feasiblity = new_bee.feasiblity
            Bees._calculating_fitness(bee, self.blocks, self.demands)

            change_flag = True
            
        elif(validality_flag_current_bee == True and validality_flag_new_bee == True):
            # validality_flag_current_bee is true here
            
            # since the feasiblities are both true we do not need to set it again
            # we need to set the new fitness
            improvement_flag = self._improvement_check(bee, new_bee)
            
            if(improvement_flag):
                bee.data = new_bee.data
                bee.fitness = new_bee.fitness
                Bees._calculating_fitness(bee, self.blocks, self.demands)
                
                change_flag = True
            
        return change_flag        
    
    def _tournoment(self, population):
        
        tournoment_list = []
        for i in range(self.k_tournoment):
            tournoment_list.append(random.choice(population))
            
        max_Fitness = -100000
        max_Bee = None
        for bee in tournoment_list:
            if(bee.fitness > max_Fitness):
                max_Fitness = bee.fitness
                max_Bee = bee
        return max_Bee
    
    def _roulette_wheel(self, population, sum_of_fitnesses):
        
        # choose a random number for selecting our bee    
        pick = random.uniform(0, sum_of_fitnesses)
        
        # selecting our bee by the "pick" number and roulette wheel procedure
        current = 0
        for bee in population:
            current += bee.fitness
            if current >= pick:
                return bee         
                
    def _cross_over_one_point(self, population, bee):
        # for each answer that employed bees have made, we select a radom neighbor
        # for each answer we also select a random position, and it replaced with its neighbors pos
        # if the changed answer be better than the previous one and it be valid, it will change
        # we also return that if the cross-over has done a change or not
        
        x = random.random()

        if(x<=self.crossover_probbility):
            term_pos = random.randint(1, self.demands_amount-1)
            neighbor_bee = random.choice(population)
            self.replace_terms(bee, neighbor_bee, term_pos)
        
    def replace_terms(self, bee, neighbor_bee, random_pos):
        # in here we change parts of our choromosome base on choosed term
        
        data = []
        for i in range(0, random_pos):
            data.append(bee.data[i])
        for j in range(random_pos, self.demands_amount):
            data.append(neighbor_bee.data[j])
        
        bee.data = data
                                                            
    def _mutation(self, bee):
        # for each answer that employed bees have made, we select a random position and we change it with 0 or 1 (randomly)
        # only if the changed answer be better than the previous one and it be valid, it will change
        # we also return that if the muatation has done a change or not
        
        for i in range(self.demands_amount):            
            x = random.random()
            if(x<=self.mutation_probblity):
                bee.data[i] = self._make_demand_answer(self.demands[i])
                
    def _improvement_check(self, current_bee, new_bee):
        # checking that the new bee (changed bee by cross_over or mutation) has imporoved or not
        
        Bees._calculating_fitness(current_bee, self.blocks, self.demands)
        Bees._calculating_fitness(new_bee, self.blocks, self.demands)
        return True if new_bee.fitness>current_bee.fitness else False
    
    def finding_best_bee(self, population):
        # finding the best solution, with best fitness
        # the answer must be feasible
        
        best_fitness = -1000000
        best_bee = None
        for bee in population:
            # if(bee.fitness == None):
            Bees._calculating_fitness(bee, self.blocks, self.demands)
            if((bee.feasiblity==True) and (bee.fitness>best_fitness)):
                best_fitness = bee.fitness
                best_bee = bee

        return best_bee, best_fitness
    
    def validality_amount(self, population):
        invalid_amount = 0
        for i in population:
            if (i.feasiblity == False):
                invalid_amount += 1
        population_amount = len(population)
        valid_amount = population_amount - invalid_amount
        print(f"amount of invalid data: {invalid_amount}")        
        print(f"amount of valid data: {valid_amount}")        
        print(f"total population: {population_amount}")        
