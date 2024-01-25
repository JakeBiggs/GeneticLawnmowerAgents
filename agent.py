import random


class Agent:
    def __init__(self, position, lawn_size):
        self.position = position
        self.previous_position = position
        self.lawn_size = lawn_size
        self.fitness = 0
        self.individual = []

    def get_moveset(self):
        return self.individual

    def move(self, position, firstGen, move_index=None):
        # Define the directions the agent can move in
        directions = [(-1, 0),  # Up
                      (1, 0),   # Down
                      (0, -1),  # Left
                      (0, 1)]   # Right

        self.position = position

        if not firstGen:
            #print("SELF.INDIVIDUAL: ",self.individual)
            if len(self.individual) > 0:

                move = self.individual[move_index]
                # Calculate the new position
                new_position = ((self.position[0] + directions[move][0]) % self.lawn_size, 
                                (self.position[1] + directions[move][1]) % self.lawn_size)
                
                # Update the agent's position
                self.previous_position = self.position
                self.position = new_position
                
                # Update position with new_position
                position = new_position
                
                print("New position:", new_position)

        else: 
            # Choose a random direction
            choice = random.choice(range(4))

            # Calculate the new position
            new_position = ((self.position[0] + directions[choice][0]) % self.lawn_size, 
                            (self.position[1] + directions[choice][1]) % self.lawn_size)

            # Update the position
            self.previous_position = self.position
            self.position = new_position
            self.individual.append(choice)  # Update the individual attribute with the new move
            
            # Update position with new_position
            #self.position = new_position
            
        """
        if not firstGen:
            #print(self.individual[0])
            print("SELF.INDIVIDUAL: ",self.individual)
            for index in self.individual[0]:
                print("INDEX=",index)
                direction = index

                # Calculate the new position
                new_position = (self.position[0] + directions[direction][0], self.position[1] + directions[direction][1])
                
                # Check if the new position is within bounds
                if 0 <= new_position[0] < self.lawn_size and 0 <= new_position[1] < self.lawn_size:
                    # Update the agent's position
                    self.previous_position = position
                    self.position = new_position
                
                print("Current position:", self.position)
                print("New position:", new_position)
                # Check if the new position is within the lawn
                if 0 <= new_position[0] < self.lawn_size and 0 <= new_position[1] < self.lawn_size:
                    # Update the position
                    self.previous_position = self.position
                    self.position = (max(min(new_position[0], self.lawn_size - 1), 0),
                                    max(min(new_position[1], self.lawn_size - 1), 0))
                else:
                    self.previous_position = self.position
        else: 
            # Choose a random direction
            choice = random.choice(range(4))

            # Calculate the new position
            new_position = (self.position[0] + directions[choice][0], self.position[1] + directions[choice][1])

            # Check if the new position is within the lawn
            if 0 <= new_position[0] < self.lawn_size and 0 <= new_position[1] < self.lawn_size:
                # Update the position
                self.previous_position = self.position
                self.position = new_position
                self.individual.append(choice)  # Update the individual attribute with the new move
            else:    
                # Move the agent to a valid position
                self.previous_position = self.position
                self.position = (max(min(new_position[0], self.lawn_size - 1), 0),
                                    max(min(new_position[1], self.lawn_size - 1), 0))
                self.individual.append(choice)  # Update the individual attribute with the new move
            #====================================
            #Check if the agent is in the middle of the lawn
            if position[0] > 0 and position[0] < 9 and position[1] > 0 and position[1] < 9:
                #Choose a random direction
                choice = random.choice(range(4))
            # Edge cases
            elif position[0] == 0:
                if position[1] == 0:
                    # Choose between down and right
                    choice = random.choice([1, 3])
                elif position[1] == 9:
                    # Choose between down and left
                    choice = random.choice([1, 2])
                else:
                    # Choose between down, left, and right
                    choice = random.choice([1, 2, 3])

            elif position[0] == 9:
                if position[1] == 0:
                    # Choose between up and right
                    choice = random.choice([0, 3])
                elif position[1] == 9:
                    # Choose between up and left
                    choice = random.choice([0, 2])
                else:
                    # Choose between up, left, and right
                    choice = random.choice([0, 2, 3])

            elif position[1] == 0:
                # Choose between up, down, and right
                choice = random.choice([0, 1, 3])

            elif position[1] == 9:
                # Choose between up, down, and left
                choice = random.choice([0, 1, 2])


            #Update positions based on choice
            self.individual.append(choice)
            self.previous_position = self.position
            self.position = (self.position[0] + directions[choice][0], self.position[1] + directions[choice][1])
            
            return choice
            """