import PySimpleGUI as sg
import time, csv, os
from agent import Agent
from algorithm import GeneticAlgorithm
global WINDOW_SIZE; WINDOW_SIZE = (800,600)

#Genetic Algorithm Parameters
global NUM_OF_GENERATIONS; NUM_OF_GENERATIONS = 1000
global POPULATION_SIZE; POPULATION_SIZE = 100
global STEPS_NUMBER; STEPS_NUMBER = 100
global current_generation; current_generation = []
global generation_metrics; generation_metrics = {}
global all_generation_metrics; all_generation_metrics = []

#Define gamestates
def main_menu_state():
    # Define the window's contents
    layout = [
        [sg.VerticalSeparator(pad=((0,0),(0,100)))], 
        [sg.Text("Genetic Programming for the Lawn Mower Problem", justification='center', size=(50,1), font=("Helvetica", 25))],
        [sg.Column([[sg.Image(filename="mowerpng.png")]], justification='center')],
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
        [sg.Text(f"Generation Number: {generation_number}", key="generation_number", size=(20,1))],
        [sg.Text(f"% Of Lawn Mowed: {mowed_cells_percentage}", key="mowed_cells_percent", size=(20,1))],
        [sg.Text(f"Agent Number: {agent_number}", key="agent_number", size=(20,1))],
        [sg.Text(f"Step Number: {step_number}", key="step_number", size=(20,1))]
    ]

    # Create the buttons
    buttons_row = [
        sg.Button("Start", size=(10,1)), 
        sg.Button("Reset", size=(10,1)), 
        sg.Button('Quit', size=(10,1))
    ]

    # Create the layout
    layout = [
        [sg.Column(text_elements), sg.Column(grid)],
        [sg.Column([buttons_row], justification='center')],
        [sg.Slider(range=(0,0.5),resolution=0.01, default_value=0, size=(50,20), orientation="horizontal",enable_events=True, disable_number_display=True, key="slider")],
        [sg.Text("Model Performance: ", size=(50,1), key="model_performance")]
    ]

    # Create the window
    window = sg.Window('COMP213 - Lawn Mower Problem', layout, size=WINDOW_SIZE)

    #Event Loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            window.close()
            return 'QUIT_STATE'
        elif event == 'Quit':
            window.close()
            return 'MAIN_MENU_STATE'
        elif isinstance(event, tuple): #Our button presses are stored as tuples
            
           if event not in mowed_cells:
                mowed_cells.append(event) #Add the button press to the list of mowed cells
                window[event].update(button_color=('light green'))
                mowed_cells_count += 1 #Increment the number of mowed cells
                mowed_cells_percentage = (mowed_cells_count / (lawn_size**2)) * 100
                window['mowed_cells_percent'].update(f"% Of Lawn Mowed:{mowed_cells_percentage}") #Update the text element
        elif event == 'Start':
            agent_number = 1

            window['agent_number'].update(f"Agent Number:{agent_number}")
            agents = [Agent((0,0), lawn_size) for _ in range(POPULATION_SIZE)]
            window['generation_number'].update(f"Generation Number:{generation_number}")
            for g in range(NUM_OF_GENERATIONS):
                generation_number += 1
                window['generation_number'].update(f"Generation Number:{generation_number}")
                if generation_number >1:
                    print("Movesets after next loop:", [agent.individual for agent in agents])  
                for a in range(POPULATION_SIZE):
                    visited_cells = []
                    reset_lawn(window, lawn_size)
                    
                    step_number = 0
                    window['step_number'].update(f"Step Number:{step_number}")
                                    
                    for i in range(STEPS_NUMBER):
                        

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
                        if generation_number == 1:
                            agent.move(agent.position, firstGen=True)
                            step_number += 1
                            
                            window['step_number'].update(f"Step Number:{step_number}")
                    
                            if agent.previous_position not in visited_cells:
                                window[agent.previous_position].update(button_color=('light green'))
                                visited_cells.append(agent.previous_position)
                            else:
                                window[agent.previous_position].update(button_color=('light green')) 
                            window[agent.position].update(button_color=('black'))
                            
                            if agent.position not in mowed_cells:
                                mowed_cells.append(agent.position)
                                mowed_cells_count += 1
                                mowed_cells_percentage = (mowed_cells_count / (lawn_size**2)) * 100
                                window['mowed_cells_percent'].update(f"% Of Lawn Mowed:{mowed_cells_percentage}")
                        
                        else:
                            
                            agent.move(agent.position, firstGen=False, move_index=i)
                            #time.sleep(0.1)
                            step_number += 1
                            window['step_number'].update(f"Step Number:{step_number}")
                        
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
                                    sg.popup("Lawn Mowed!")
                                mowed_cells_percentage = (mowed_cells_count / (lawn_size**2)) * 100
                                window['mowed_cells_percent'].update(f"% Of Lawn Mowed:{mowed_cells_percentage}")
                                window.refresh()
                        time.sleep(float(values['slider']))
                        #time.sleep(0.01)
                
                    agent_number += 1
                    current_generation.append((agent.individual, mowed_cells_count))
                    window['agent_number'].update(f"Agent Number:{agent_number}")                  
                    
                    agent.position = (0,0)
                    agent.previous_position = (0,0)
                    window.refresh()
                ### ==========GENERATION ENDS HERE=========== ###
                
                #Storing data from this generation before evoultion
                fitness_scores= [current_generation[i][1] for i in range(len(current_generation))]
                best_fitness= max(fitness_scores)
                average_fitness= sum(fitness_scores)/len(fitness_scores)
                diversity= len(set(fitness_scores))

                #Store the metrics for the current generation
                generation_metrics ={
                    'generation_number': generation_number,
                    'best_fitness': best_fitness,
                    'average_fitness': average_fitness,
                    'diversity': diversity,
                    'individuals': current_generation
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
                all_generation_metrics.append(generation_metrics)

                if generation_number >0:

                        #Evolving the current generation
                        movesets = next_generation()
                        print("Movesets before assignment:", movesets)
                        #sg.popup("Next Generation")
                        
                        for i, agent in enumerate(agents):
                            #print("Moveset:", movesets[i])
                            agent.individual = movesets[i]
                            agent.position = (0,0)
                            agent.previous_position = (0,0)
                            
                        print("Movesets after assignment:", [agent.individual for agent in agents])    
                              
        elif event == "Reset":
            reset_lawn(window, lawn_size)
            return 'MAIN_STATE'    
def quit_state():
    exit()

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
    print("Current generation evoloving")
    return ga.evolve()
    

if __name__ == "__main__":
    state = 'MAIN_MENU_STATE'
    states = { 'MAIN_MENU_STATE': main_menu_state, 'MAIN_STATE': main_state, 'QUIT_STATE': quit_state }
    
    while True:
        if state:
            state = states[state]()
            if state == None:
                break