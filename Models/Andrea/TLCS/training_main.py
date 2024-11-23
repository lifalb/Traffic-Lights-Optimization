from __future__ import absolute_import
from __future__ import print_function

import os
import datetime
from shutil import copyfile
import pandas as pd
from training_simulation import Simulation
#changed from generator to generate Y
from generate import TrafficGenerator
from memory import Memory
from model import TrainModel
from visualization import Visualization
from utils import import_train_configuration, set_sumo, set_train_path

# Define your SUMO configuration file (.sumocfg) path (without file name, define file name in training_settings.ini)
sumocfg_root_file_path = os.path.join(os.pardir, os.pardir,os.pardir, "training_network")

# Define the route file of the output files (where you want to keep the output files)
output_csv_root_path = os.path.join(os.pardir, os.pardir,os.pardir, "outputs - train", "Andrea/episodes/")

if __name__ == "__main__":

    config = import_train_configuration(config_file='training_settings.ini')

    sumo_cmd = set_sumo(config['gui'],sumocfg_root_file_path, config['sumocfg_file_name'], config['max_steps'])
    path = set_train_path(config['models_path_name'])

    Model = TrainModel(
        config['num_layers'], 
        config['width_layers'], 
        config['batch_size'], 
        config['learning_rate'], 
        input_dim=config['num_states'], 
        output_dim=config['num_actions']
    )

    Memory = Memory(
        config['memory_size_max'], 
        config['memory_size_min']
    )

    TrafficGen = TrafficGenerator(
        config['num_of_seconds'], 
        config['output_file_name']
    )

    Visualization = Visualization(
        path, 
        dpi=96
    )
        
    Simulation = Simulation(
        Model,
        Memory,
        TrafficGen,
        sumo_cmd,
        config['gamma'],
        config['max_steps'],
        config['green_duration'],
        config['yellow_duration'],
        config['num_states'],
        config['num_actions'],
        config['training_epochs']
    )
    
    episode = 0
    timestamp_start = datetime.datetime.now()
    
    while episode < config['total_episodes']:
        print('\n----- Episode', str(episode+1), 'of', str(config['total_episodes']))
        epsilon = 1.0 - (episode / config['total_episodes'])  # set the epsilon for this episode according to epsilon-greedy policy
        simulation_time, training_time = Simulation.run(episode, epsilon)  # run the simulation
        print('Simulation time:', simulation_time, 's - Training time:', training_time, 's - Total:', round(simulation_time+training_time, 1), 's')
        episode += 1
        data = {
            'episode' : [episode],
            'reward':[Simulation.reward_store[-1]],
            'accumulated_wait_times' : [Simulation.accumulated_wait_times[-1]],
            'accumulated_avg_wait_times' : [Simulation.accumulated_avg_wait_times[-1]],
            'accumulated_queue_length' : [Simulation.accumulated_queue_length[-1]],
            'accumulated_avg_queue_length' : [Simulation.accumulated_avg_queue_length[-1]],
            'accumulated_total_fuel_consumption' : [Simulation.accumulated_total_fuel_consumption[-1]],
            'accumulated_avg_fuel_consumption' : [Simulation.accumulated_avg_fuel_consumption[-1]],
            'accumulated_pedestrian_wait_times' : [Simulation.accumulated_pedestrian_wait_times[-1]],
            'accumulated_pedestrian_avg_wait_times' : [Simulation.accumulated_pedestrian_avg_wait_times[-1]],
        }
        df = pd.DataFrame(data)
        # Save the DataFrame to a CSV file
        output_csv = f"{output_csv_root_path}/output_values_ep_{episode}.csv"
        df.to_csv(output_csv, index=False)
        Model.save_model(path)

    print("\n----- Start time:", timestamp_start)
    print("----- End time:", datetime.datetime.now())
    print("----- Session info saved at:", path)

    Model.save_model(path)

    copyfile(src='training_settings.ini', dst=os.path.join(path, 'training_settings.ini'))
    Visualization.save_data_and_plot(data=Simulation.reward_store, filename='reward', xlabel='Episode', ylabel='Cumulative negative reward')
    Visualization.save_data_and_plot(data=Simulation.accumulated_wait_times, filename='Acc_Wait_time', xlabel='Episode', ylabel='Accumulated Wait Times')
    Visualization.save_data_and_plot(data=Simulation.accumulated_avg_wait_times, filename='acc_avg_wait_time', xlabel='Episode', ylabel='Accumulated Average Wait Times')
    Visualization.save_data_and_plot(data=Simulation.accumulated_queue_length, filename='acc_queue_len', xlabel='Episode', ylabel='Accumulated Queue Length')
    Visualization.save_data_and_plot(data=Simulation.accumulated_avg_queue_length, filename='acc_avg_queue_len', xlabel='Episode', ylabel='Accumulated Avegrage Queue Length')
    Visualization.save_data_and_plot(data=Simulation.accumulated_total_fuel_consumption , filename='acc_total_fuel_con', xlabel='Episode', ylabel='Accumulated total Fuel Consumption')
    Visualization.save_data_and_plot(data=Simulation.accumulated_avg_fuel_consumption, filename='acc_avg_fuel_con', xlabel='Episode', ylabel='Accumulated Average Fuel Consumption')
    Visualization.save_data_and_plot(data=Simulation.accumulated_pedestrian_wait_times , filename='acc_ped_wait_time', xlabel='Episode', ylabel='Accumulated Pedestrian Wait Times')
    Visualization.save_data_and_plot(data=Simulation.accumulated_pedestrian_avg_wait_times, filename='acc_ped_avg_wait_time', xlabel='Episode', ylabel='Accumulated Pedestrian Average Wait Times')