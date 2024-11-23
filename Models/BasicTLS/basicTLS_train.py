import traci
import pandas as pd
from fastprogress import progress_bar
import os

# Define your SUMO configuration file (.sumocfg) path
sumo_config = os.path.join(os.pardir, os.pardir, "training_network", "osm.sumocfg")

# Define the route file of the output files (where you want to keep the output files)
output_csv_root_path = os.path.join(os.pardir, os.pardir, "outputs - train", "BasicTLS/")

# Define number of steps
num_steps = 9600

# Define number of episodes
num_of_episodes = 150

accumulated_wait_times = []
accumulated_avg_wait_times = []
accumulated_queue_length = []
accumulated_avg_queue_length = []
accumulated_total_fuel_consumption = []
accumulated_avg_fuel_consumption = []
accumulated_pedestrian_wait_times = []
accumulated_pedestrian_avg_wait_times = []

for episode in progress_bar(range(num_of_episodes)):
    # start new connection with each episode
    sumo_cmd = ["sumo", "-c", sumo_config]  
    traci.start(sumo_cmd)
    # statistics for this episode
    total_number_of_vehciles = 0
    total_waiting_time = 0
    total_queue_length = 0
    total_fuel_consumption = 0

    total_number_of_pedestrians = 0
    total_pedestrian_waiting_time = 0
    for step in range(num_steps):
        traci.simulationStep()  # Advance one simulation step
        # Get info for each vehicle/ and queue
        departed_vehicles = traci.simulation.getDepartedIDList()
        total_number_of_vehciles += len(departed_vehicles)
        vehicle_ids = traci.vehicle.getIDList()
        step_queue_length = 0 
        for vehicle in vehicle_ids:
            if traci.vehicle.getSpeed(vehicle) < 0.1:
                step_queue_length += 1
            total_fuel_consumption += traci.vehicle.getFuelConsumption(vehicle)

        total_waiting_time += step_queue_length
        total_queue_length += step_queue_length

        # pedesetrians info
        departed_pedestrians = traci.simulation.getDepartedPersonIDList()
        total_number_of_pedestrians += len(departed_pedestrians)
        pedestrian_ids = traci.person.getIDList()
        step_pedestrian_queue_length = 0
        for pedestrian in pedestrian_ids:
            # Check if the pedestrian's speed is near zero (indicating they're queued)
            if traci.person.getSpeed(pedestrian) < 0.1:
                step_pedestrian_queue_length += 1
        # Update the total waiting time and queue length for pedestrians
        total_pedestrian_waiting_time += step_pedestrian_queue_length

        # Caluculating the evaluation metrics every five simulation steps to replicate the caluclations in the other two models
        traci.simulationStep()
        traci.simulationStep()
        traci.simulationStep()
        traci.simulationStep()
    average_queue_length = total_queue_length / num_steps
    average_waiting_time = total_waiting_time / total_number_of_vehciles
    average_fuel_consumption = total_fuel_consumption / total_number_of_vehciles
    average_pedestrain_waiting_time=(total_pedestrian_waiting_time/total_number_of_pedestrians) if total_number_of_pedestrians > 0  else 0
    accumulated_wait_times.append(total_waiting_time)
    accumulated_avg_wait_times.append(average_waiting_time)
    accumulated_queue_length.append(total_queue_length)
    accumulated_avg_queue_length.append(average_queue_length)
    accumulated_total_fuel_consumption.append(total_fuel_consumption)
    accumulated_avg_fuel_consumption.append(average_fuel_consumption)
    accumulated_pedestrian_wait_times.append(total_pedestrian_waiting_time)
    accumulated_pedestrian_avg_wait_times.append(average_pedestrain_waiting_time)
    # close connection after each episode
    traci.close()
data = {
    'accumulated_wait_times': accumulated_wait_times,
    'accumulated_avg_wait_times': accumulated_avg_wait_times,
    'accumulated_queue_length': accumulated_queue_length,
    'accumulated_avg_queue_length': accumulated_avg_queue_length,
    'accumulated_total_fuel_consumption' : accumulated_total_fuel_consumption, 
    'accumulated_avg_fuel_consumption' : accumulated_avg_fuel_consumption,
    'accumulated_pedestrian_wait_times':accumulated_pedestrian_wait_times,
    'accumulated_pedestrian_avg_wait_times' : accumulated_pedestrian_avg_wait_times
}

df = pd.DataFrame(data)
df.insert(0, 'episode', df.index)
output_csv_path = f'{output_csv_root_path}outputs.csv'
df.to_csv(output_csv_path, index=False)
