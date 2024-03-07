import random

class GeneticAlgorithm:
    def __init__(self, population):
        self.generations = []
        #Converts population list to list of dictionaries with fitness as key and moves as value
        self.population = [{"fitness":population[1],"moveset":population[0]} for population in population ]
        
        self.population_size = len(population)
        self.mutation_rate = 0.05
        pass

    def get_fitness(self, agent):    
        return agent["fitness"]
    
    def set_options(self, crossover_method, selection_method, mutation_rate):
        self.crossover_method = crossover_method
        self.selection_method = selection_method
        self.mutation_rate = mutation_rate


    #Ranks the agents of the population based on fitness
    #population: list of agents
    #agent: list of moves
    def evaluation(self):
        self.total_fitness = 0
        ranked_population = self.population
        for agent in ranked_population:
            agent["fitness"] = self.get_fitness(agent=agent)
            self.total_fitness += agent["fitness"]
        ranked_population.sort(reverse=True, key=lambda x: x["fitness"])
        return ranked_population
            
            


    #=========SELECTION METHODS=========

    def tournament_selection(self, population, tournament_size):
        if len(population) < tournament_size:
            raise ValueError("Tournament size is larger than the population size")

        chosen_agents = []
        
        
        while len(chosen_agents) < 2:
            
            # Select a random sample of agents for the tournament
            tournament = random.sample(population, tournament_size)
            # Sort the tournament
            tournament.sort(reverse=True, key=lambda x: x["fitness"])
            chosen_agents.append(tournament[0])
            """
            agent1 = random.choice(tournament)
            agent2 = random.choice(tournament)
            if agent1["fitness"] > agent2["fitness"]:
                chosen_agents.append(agent1)
            else:
                chosen_agents.append(agent2)
            """
        return chosen_agents
        
    def roulette_selection(self, population):
        # Calculate the selection probabilities if they haven't been calculated yet this generation
        #this helped improve performance instead of calculating it every time
        if not hasattr(self, 'selection_probabilities'):
            total_fitness = sum(agent["fitness"] for agent in population)
            self.selection_probabilities = [agent["fitness"] / total_fitness for agent in population]
            #print("SELECTION PROBABILITIES: ",self.selection_probabilities)
         
        chosen_agents = random.choices(population, weights=self.selection_probabilities, k=2)
        
        #chosen_agents = []
       # while len(chosen_agents) < 2:
        #    selected = random.choices(population, weights=selection_probabilities, k=1)[0]
        #   if selected not in chosen_agents:
        #        chosen_agents.append(selected)

        return chosen_agents
        

    #Selects the best agents of the population using chosen selection method
    def selection(self,selection_method):
        
        if selection_method.lower()=="tournament":
            return self.tournament_selection(self.population, int(len(self.population)/20))
        elif selection_method.lower()=="roulette":
            return self.roulette_selection(self.population)

    #Crossover the selected agents using single or multi-point crossover
    def crossover(self, agent1, agent2,crossover_method):
        # Check that the parents are lists of moves
        #if not isinstance(parent1, list) or not isinstance(parent2, list):
         #   raise ValueError("Parent is not a list of moves")
        if len(agent1) != len(agent2):
            raise ValueError("One or both parents have fewer genes than the crossover point")
        
        #Initialise offspring and parents
        parent1 = agent1[:]
        parent2 = agent2[:]
        
        offspring1 = []
        offspring2 = []
        self.crossover_methods = ["singlepoint",
                             "multipoint"]
        
        if crossover_method.lower() == "singlepoint":
            # Choose a random crossover point
            crossover_point = random.randint(1, len(parent1) - 1)

            # Create the offspring by swapping genes after the crossover point
            offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
            offspring2 = parent2[:crossover_point] + parent1[crossover_point:]

            return offspring1, offspring2

        elif crossover_method.lower() == "multipoint":        
            # Generate a set of unique random crossover points
            #num_crossover_points = random.randint(1, len(parent1) - 1 // 2)
            num_crossover_points = len(parent1) // 10
            # Sort the crossover points
            crossover_points = sorted(random.sample(range(1, len(parent1)), num_crossover_points))
            offspring1, offspring2 = [], []
            
            # Add an extra point at the end of the chromosome
            crossover_points.append(len(parent1))
            
            # Initialize the start point
            start = 0
            
            # Loop through each section
            for i in range(len(crossover_points)):
                end = crossover_points[i]
                
                # If i is even, copy the section from parent1 to offspring1 and from parent2 to offspring2
                if i % 2 == 0:
                    offspring1.extend(parent1[start:end])
                    offspring2.extend(parent2[start:end])
                # If i is odd, copy the section from parent2 to offspring1 and from parent1 to offspring2
                else:
                    offspring1.extend(parent2[start:end])
                    offspring2.extend(parent1[start:end])
                
                # Update the start point
                start = end
            
            return offspring1, offspring2

            """
            crossover_points = set(random.randint(0, len(parent1) - 1) for _ in range(num_crossover_points))

            # Loop through each gene in the parents
            for i in range(len(parent1)):
                # If the current index is a crossover point, swap the parents
                if i in crossover_points:
                    offspring1.append(parent2[i])
                    offspring2.append(parent1[i])
                else:
                    offspring1.append(parent1[i])
                    offspring2.append(parent2[i])
            return offspring1, offspring2
        """
        if offspring1 == parent1 or offspring2 == parent2:
            raise RuntimeError("No crossover")
            

            

    def mutation(self,agent, mutation_rate):
        # Check that the agent is a list of moves
        agent = agent[:]
        if not isinstance(agent, list):
            raise ValueError("Agent is not a list of moves")

        #Loop through each gene in the agent
        for i in range(len(agent)):
            #If the mutation rate is reached, mutate the gene
            if random.random() < mutation_rate:
                agent[i] = random.choice(range(4))

        return agent
    
    def evolve(self, selection_method, crossover_method, mutation_rate):
        next_generation_movesets = []

        #Set selected options
        self.set_options(crossover_method, selection_method, mutation_rate)

        #Sort the population by fitness
        self.population = self.evaluation()

        while len(next_generation_movesets) < self.population_size:
            
            # Select best agents for crossover
            parents = self.selection(selection_method=self.selection_method)
            
            # Remove the fitnesses from the parents
            parents = [parent['moveset'] for parent in parents]

            # Crossover the parents
            offspring1, offspring2 = self.crossover(parents[0], parents[1], crossover_method=self.crossover_method)

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

        # Delete the selection probabilities so they get recalculated for the next generation
        # Helps improve performance so do not have to recalculate every call
        if hasattr(self, 'selection_probabilities'):
            del self.selection_probabilities

        
        # Update the population
        return next_generation_movesets