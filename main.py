import PySimpleGUI as sg
import time, csv, os
from agent import Agent
from algorithm import GeneticAlgorithm
global WINDOW_SIZE; WINDOW_SIZE = (800,600)

#Genetic Algorithm Parameters
global NUM_OF_GENERATIONS; NUM_OF_GENERATIONS = 1000
global POPULATION_SIZE; POPULATION_SIZE = 100
global STEPS_NUMBER; STEPS_NUMBER = 100
global genome_length; genome_length = 10
global current_generation; current_generation = []
global generation_metrics; generation_metrics = {}
global all_generation_metrics; all_generation_metrics = []

#Define gamestates
def main_menu_state():
    sg.theme('DarkGreen')
    #sg.theme('DarkAmber')
    # Define the window's contents
    layout = [
        [sg.VerticalSeparator(pad=((0,0),(0,100)))], 
        [sg.Text("Genetic Programming: The Lawn Mower Problem", justification='center', size=(50,1), font=("Verdana", 20))],
        [sg.Column([[sg.Image(filename="mowerpng.png")]], justification='center')],
        [sg.Column([[sg.Text("By Jacob Biggs", justification='center', size=(50,1), font=("Courier", 12))]], justification='center')],
        [sg.VerticalSeparator(pad=((0,0),(0,50)))],  # Add vertical space before buttons
        [sg.Column([[sg.Button('Start'), sg.Button('Quit')]], justification='center')]  # Center the buttons
    ]
    
    # Create the window
    window = sg.Window('Main Menu', layout, size=WINDOW_SIZE)
    
    # Event Loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the Quit button
        if event == sg.WINDOW_CLOSED or event == 'Quit':
            window.close()
            return 'QUIT_STATE'
        elif event == 'Start':
            window.close()
            return 'MAIN_STATE'

def main_state():
    # Define the window's layout for our lawn
    layout = []
    lawn_size = 10
    cell_size = (2,1)

    #Define variables for the genetic algorithm
    generation_number = 0
    step_number = 0
    agent_number = 0
    model_performance = "Highest Average Fitness: 0, Highest Best Fitness: 0, Current Average Fitness: 0"

    #Define variables for the environment
    global mowed_cells; mowed_cells = []
    global mowed_cells_count; mowed_cells_count = 0
    global mowed_cells_percentage; mowed_cells_percentage = 0
    
    # Create the grid for the lawn
    grid = []
    for i in range(lawn_size):
        row = []
        for j in range(lawn_size):
            row.append(sg.Button('', size=cell_size, key=(i,j), button_color=('green')))
        grid.append(row)

    # Create the text elements
    text_elements = [
        [sg.Text(f"Generation Number: {generation_number}", key="generation_number", size=(20,1),font=("Verdana", 12))],
        [sg.Text(f"% Of Lawn Mowed: {mowed_cells_percentage}", key="mowed_cells_percent", size=(20,1),font=("Verdana", 12))],
        [sg.Text(f"Agent Number: {agent_number}", key="agent_number", size=(20,1),font=("Verdana", 12))],
        [sg.Text(f"Step Number: {step_number}", key="step_number", size=(20,1),font=("Verdana", 12))]
    ]

    # Create the buttons
    buttons_row = [
        sg.Button("Start", size=(10,1)), 
        sg.Button("Reset", size=(10,1)), 
        sg.Button('Quit', size=(10,1))
    ]
    
    #Leaderboard section
    #remove_duplicates(filename="leaderboard.csv")
    leaderboard_agents = load_agents_from_csv()
    agent_strings = ["Solution " + str(i+1) for i in range(len(leaderboard_agents))]
    leaderboard_layout = [ sg.Listbox(values=agent_strings, size=(20,10), key="leaderboard", enable_events=True)]
    
    

    #Metrics section
    metrics_layout = [
                    [sg.Text(f"Model Performance: ", size=(70,3), font=("Verdana", 12),key="model_performance")],
                    [sg.Text(f"Highest Average Fitness: None, Last Generation Average Fitness: None", size=(70,2),font=("Verdana", 12), key="average_fitnesses")],
                    [sg.Text(f"Highest Best Fitness: None, Last Generation Best Fitness: None", size=(70,2),font=("Verdana", 12), key="best_fitnesses")]
    ]
    
    # Create the layout
    layout = [
        [sg.Column(text_elements), sg.Column(grid), sg.Column([[sg.Text("Past Solutions: ")],leaderboard_layout])],
        [sg.Column([buttons_row], justification='center')],
        [sg.Column([[sg.Slider(range=(0.5,0),resolution=0.01, default_value=0.25, size=(50,20), orientation="horizontal",enable_events=True, disable_number_display=True, key="slider")]], justification='center')],
        [sg.Column(metrics_layout, justification='center')]   
    ]
        
    # Create the window
    window = sg.Window('COMP213 - Lawn Mower Problem', layout, size=WINDOW_SIZE)
    
    
    running = False
    #Event Loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
            return 'QUIT_STATE'
        elif event == 'Quit':
            window.close()
            return 'MAIN_MENU_STATE'
        elif event == 'leaderboard':
            if not running:
                #An agent has been selected from the leaderboard
                leaderboard_index=  int(values['leaderboard'][0].split(" ")[1])-1
                selected_agent = leaderboard_agents[leaderboard_index]
                print(">Agent number "+str(leaderboard_index), "seclected from leaderboard!")

                visited_cells = []
                mowed_cells= []
                for i in range(STEPS_NUMBER):
                    values = check_events(window)
                    selected_agent.move(selected_agent.position, move_index=i % len(selected_agent.individual))
                    if selected_agent.previous_position not in visited_cells:
                        window[selected_agent.previous_position].update(button_color=('light green'))
                        visited_cells.append(selected_agent.previous_position)
                    else:
                        window[selected_agent.previous_position].update(button_color=('light green'))  
                    window[selected_agent.position].update(button_color=('black'))
                    window.refresh()

                    if selected_agent.position not in mowed_cells:
                        mowed_cells.append(selected_agent.position)
                        mowed_cells_count += 1
                        if mowed_cells_count == 100:
                            sg.popup("Agent Complete: Lawn Mowed!")
                            reset_lawn(window, lawn_size)
                    time.sleep(float(values['slider']))
                    

        elif isinstance(event, tuple): #Our button presses are stored as tuples
           if event not in mowed_cells and not running:
                mowed_cells.append(event) #Add the button press to the list of mowed cells
                window[event].update(button_color=('light green'))
                mowed_cells_count += 1 #Increment the number of mowed cells
                mowed_cells_percentage = round((mowed_cells_count / (lawn_size**2)) * 100, 2)
                window['mowed_cells_percent'].update(f"% Of Lawn Mowed:{mowed_cells_percentage}") #Update the text element
        
        elif event == 'Start':
            running = True
            agent_number = 1
            window['agent_number'].update(f"Agent Number:{agent_number}")
            agents = [Agent((0,0), lawn_size, genome_length=genome_length) for _ in range(POPULATION_SIZE)]
            
            window['generation_number'].update(f"Generation Number:{generation_number}")

            #First generation
            highest_average_fitness = 0
            highest_best_fitness = 0

            for g in range(NUM_OF_GENERATIONS):
                generation_number += 1
                window['generation_number'].update(f"Generation Number:{generation_number}")
                
                for a in range(POPULATION_SIZE):
                    visited_cells = []
                    reset_lawn(window, lawn_size)
                    step_number = 0
                    window['step_number'].update(f"Step Number:{step_number}")
                                    
                    for i in range(STEPS_NUMBER):
                        step_number += 1
                        window['step_number'].update(f"Step Number:{step_number}")

                        event, values = window.read(timeout=0)
                        if event == "Reset":
                            window.close()
                            return 'MAIN_STATE'
                        elif event == "Quit":
                            window.close()
                            return 'MAIN_MENU_STATE'
                        elif event == "slider":
                            window['slider'].update(values['slider'])
                            window.refresh()

                        agent = agents[a]                       
                        if generation_number == 1 and len(agent.individual)==0: #and i % genome_length == 0:
                            agent.individual = agent.generate_moveset()
                        if len(agent.individual) > 0:
                            agent.move(agent.position, move_index=i % len(agent.individual))

                            if agent.previous_position not in visited_cells:
                                window[agent.previous_position].update(button_color=('light green'))
                                visited_cells.append(agent.previous_position)
                            else:
                                window[agent.previous_position].update(button_color=('light green'))  
                            window[agent.position].update(button_color=('black'))
                            window.refresh()

                            if agent.position not in mowed_cells:
                                mowed_cells.append(agent.position)
                                mowed_cells_count += 1
                                if mowed_cells_count == 100:
                                    save_moveset_to_csv({'moveset': agent.individual}, 'leaderboard.csv', fieldnames=['moveset'])
                                    remove_duplicates(filename="leaderboard.csv")
                                    leaderboard_agents = load_agents_from_csv()
                                    agent_strings = ["Solution " + str(i+1) for i in range(len(leaderboard_agents))]
                                    window['leaderboard'].update(values=[agent_strings[i] for i in range(len(leaderboard_agents))])
                                    print("Lawn Mowed, saving moveset to csv")
                                    
                                    #sg.popup("Lawn Mowed!")
                                mowed_cells_percentage = (mowed_cells_count / (lawn_size**2)) * 100
                                window['mowed_cells_percent'].update(f"% Of Lawn Mowed:{mowed_cells_percentage}")
                                window.refresh()
                        time.sleep(float(values['slider']))
                     
                    #=====MOVES HAVE BEEN MADE, EVALUATE THE AGENT'S FITNESS=====
                    agent_number += 1

                    agent.complete_rows, agent.complete_columns = count_rows_columns(mowed_cells, lawn_size)
                    agent.mowed_cells_count = mowed_cells_count
                    agent.calculate_fitness()

                    current_generation.append((agent.individual, agent.fitness))
                    window['agent_number'].update(f"Agent Number:{agent_number}")                  
                    
                    agent.position = (0,0)
                    agent.previous_position = (0,0)
                    window.refresh()
                ### ==========GENERATION ENDS HERE=========== ###
                
                #Storing data from this generation before evoultion
                fitness_scores= [current_generation[i][1] for i in range(len(current_generation))]
                best_fitness= round(max(fitness_scores),2)
                average_fitness= round(sum(fitness_scores)/len(fitness_scores),2)
                #diversity= len(set(fitness_scores))

                # Convert the movesets to strings and add them to a set
                unique_movesets = set(str(current_generation[i][0]) for i in range(len(current_generation)))

                # Calculate the diversity as the number of unique movesets
                diversity = len(unique_movesets)

                if average_fitness > highest_average_fitness:
                    highest_average_fitness = average_fitness
                if best_fitness > highest_best_fitness:
                    highest_best_fitness = best_fitness
                
                # Update the model performance text
                window['average_fitnesses'].update(f"Highest Average Fitness: {highest_average_fitness}, Last Generation Average Fitness: {average_fitness}")
                window['best_fitnesses'].update(f"Highest Best Fitness: {highest_best_fitness}, Last Generation Best Fitness: {best_fitness}")
                
                #Store the metrics for the current generation
                generation_metrics ={
                    'generation_number': generation_number,
                    'best_fitness': best_fitness,
                    'average_fitness': average_fitness,
                    'diversity': diversity,
                    'individuals': [current_generation[i][0] for i in range(len(current_generation))]
                }

                fieldnames= ['generation_number', 'best_fitness', 'average_fitness', 'diversity', 'individuals']
                if os.path.isfile('metrics.csv') == False:
                    
                    with open('metrics.csv', 'w') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writeheader()
                if os.path.isfile('metrics.csv') == True:
                    with open('metrics.csv', 'a') as csv_file:
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        writer.writerow(generation_metrics)

                #store the metrics for all generations
                #all_generation_metrics.append(generation_metrics)
        
                #Evolving the current generation
                movesets = next_generation()
                print("Generation", generation_number ,"evolving")                
                #sg.popup("Next Generation")
                
                #Reset all the agents
                for i, agent in enumerate(agents):
                    agent.individual = movesets[i]
                    agent.position = (0,0)
                    agent.previous_position = (0,0)
                current_generation.clear()    
                
        elif event == "Reset":
            reset_lawn(window, lawn_size)
            return 'MAIN_STATE'   
def quit_state():
    exit()
    
#==============HELPER FUNCTIONS=================#

def check_events(window):
    event, values = window.read(timeout=0)
    if event == "Reset":
        window.close()
        return 'MAIN_STATE'
    elif event == "Quit":
        window.close()
        return 'MAIN_MENU_STATE'
    elif event == "slider":
        window['slider'].update(values['slider'])
        window.refresh()
    return values

def count_rows_columns(mowed_cells, lawn_size):
    mowed_cells_set = (set(mowed_cells)) #Removes duplicates
    complete_rows = sum(all((i, j) in mowed_cells_set for j in range(lawn_size)) for i in range(lawn_size))
    complete_columns = sum(all((j, i) in mowed_cells_set for j in range(lawn_size)) for i in range(lawn_size))
    return complete_rows, complete_columns

def reset_lawn(window, lawn_size):
    global mowed_cells
    global mowed_cells_count
    global mowed_cells_percentage
    # Reset the lawn and mowed cells
    mowed_cells = []
    mowed_cells_count = 0
    mowed_cells_percentage = 0
    for i in range(lawn_size):
        for j in range(lawn_size):
            window[(i,j)].update(button_color=('green'))
    window['mowed_cells_percent'].update(f"% Of Lawn Mowed:{mowed_cells_percentage}")
    window.refresh()

def next_generation():
    ga = GeneticAlgorithm(current_generation)
    #current_generation.clear()
    return ga.evolve()

def save_moveset_to_csv(content, filename, fieldnames=None):
    content['moveset'] = ','.join(map(str, content['moveset']))
    if not os.path.isfile(filename) :                
            with open(filename, 'w') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

    with open(filename, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(content)

def load_agents_from_csv(filename='leaderboard.csv'):
    agents = []
    if os.path.isfile(filename):
        with open(filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                agent = Agent((0,0), lawn_size=10, genome_length=len(row['moveset']))
                moveset_str = row['moveset'].strip("[]")
                agent.individual = list(map(int,row['moveset'].strip('[]').split(',')))
                agents.append(agent)
    return agents

def remove_duplicates(filename='leaderboard.csv'):
    if os.path.isfile(filename) == True:
        # Convert the movesets to strings and add them to a set
        with open(filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            movesets = []
            for row in reader:
                movesets.append(row['moveset'])
            movesets = set(movesets) #Remove duplicates
        # Write the movesets back to the file
        with open(filename, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['moveset'])
            writer.writeheader()
            for moveset in movesets:
                writer.writerow({'moveset': moveset})




if __name__ == "__main__":
    state = 'MAIN_MENU_STATE'
    states = { 'MAIN_MENU_STATE': main_menu_state, 'MAIN_STATE': main_state, 'QUIT_STATE': quit_state }
    
    while True:
        if state:
            state = states[state]()
            if state == None:
                break