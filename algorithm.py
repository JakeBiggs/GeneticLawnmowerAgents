import random

class GeneticAlgorithm:
    def __init__(self, population):
        self.generations = []
        #Converts population list to list of dictionaries with fitness as key and moves as value
        self.population = [{"fitness":population[1],"moveset":population[0]} for population in population ]
        
        self.population_size = len(population)
        self.mutation_rate = 0.02
        pass

    def fitness(self, agent,w1,w2,lawn_size):    
        #Fitness based on just lawn mowed
        #print(agent[1])
        return agent["fitness"]
    
        #Fitness is based on combination of lawn mowed and steps taken
        #return w1 * (len(agent.mowed_cells) / (lawn_size**2)) + w2 * (1 / agent.steps_taken if agent.steps_taken != 0 else 0)
        

    #Ranks the agents of the population based on fitness
    #population: list of agents
    #agent: list of moves
    def evaluation(self):
        ranked_population = self.population
        for agent in ranked_population:
            agent["fitness"] = self.fitness(agent=agent,w1=0,w2=0, lawn_size=10)
        ranked_population.sort(reverse=True, key=lambda x: x["fitness"])
        return ranked_population
            
            #ranked_population.append(agent)
        #ranked_population.sort(reverse=True, key=lambda x: x[0])
        #return ranked_population

    #Selects the best agents of the population for crossover (elitist tournament selection)
    def selection(self, tournament_size, elite_size):
        
        if tournament_size > len(self.population) or elite_size > tournament_size:
            raise ValueError("Invalid tournament size or elite size")

        #Rank the population for tournament selection
        #ranked_population = self.evaluation(self.population)
        self.population = self.evaluation()

        #Create a tournament
        tournament = random.sample(self.population, tournament_size)
        
        #Sort the tournament
        tournament.sort(reverse=True, key=lambda x: x["fitness"])
        
        #Select elite individuals
        elites = tournament[:elite_size]
        print("ELITES: ",elites)
        return elites

    #Crossover the selected agents using single or multi-point crossover
    def crossover(self, parent1, parent2, crossover_point=3):
        # Check that the parents are lists of moves
        #if not isinstance(parent1, list) or not isinstance(parent2, list):
         #   raise ValueError("Parent is not a list of moves")
        if len(parent1) < crossover_point or len(parent2) < crossover_point:
            raise ValueError("One or both parents have fewer genes than the crossover point")
        #Initialise offspring and parents
        offspring1 = []
        offspring2 = []
        #parent1 = []
        #parent2 = []

        singlepoint = True
        multipoint = False
        if singlepoint:
            # Choose a random crossover point
            crossover_point = random.randint(1, len(parent1) - 1)

            # Create the offspring by swapping genes after the crossover point
            offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
            offspring2 = parent2[:crossover_point] + parent1[crossover_point:]

            return offspring1, offspring2

        elif multipoint:        
            #Loop through each gene in the parents
            for i in range(len(parent1)):
                #If the crossover point is reached, swap the parents
                #Works every crossover_point genes
                if i % crossover_point == 0:
                    offspring1.append(parent2[i])
                    offspring2.append(parent1[i])
                else:
                    offspring1.append(parent1[i])
                    offspring2.append(parent2[i])

            print("PARENTS: ",parent1,parent2)
            print("OFFSPRING: ",offspring1,offspring2)
            return offspring1, offspring2

    def mutation(self,agent, mutation_rate):
        # Check that the agent is a list of moves
        #agent = list(agent)
        if not isinstance(agent, list):
            raise ValueError("Agent is not a list of moves")

        

        #Loop through each gene in the agent
        for i in range(len(agent)):
            #If the mutation rate is reached, mutate the gene
            if random.uniform(0,1) <= mutation_rate:
                agent[i] = random.choice(range(4))

        #agent = tuple(agent)
        return agent
    
    def evolve(self):
        parents = []
        # Select best agents for crossover
        parents = self.selection(100, 5)
        #Converts parents list to list of moves
        # Remove the fitnesses from the parents
        
        parents = [parent['moveset'] for parent in parents]

        next_generation_movesets = parents[:]  # Copy the parents to the next generation

        # Crossover parents to create offspring
        while len(next_generation_movesets) < self.population_size:
            # Select two random parents
            parent1, parent2 = random.sample(parents,2)

            # Crossover the parents
            offspring1, offspring2 = self.crossover(parent1, parent2)

            # Add the offspring to the next generation
            
            next_generation_movesets.append(offspring1)
            if len(next_generation_movesets) < self.population_size:
                next_generation_movesets.append(offspring2)
            
            

        # If the new population is larger than the old population, remove the extra individuals
        if len(next_generation_movesets) > self.population_size:
            next_generation_movesets = next_generation_movesets[:self.population_size]

        # Mutate the offspring
        for i in range(len(next_generation_movesets)):
            next_generation_movesets[i] = self.mutation(next_generation_movesets[i], self.mutation_rate)

        
        # Update the population
        return next_generation_movesets