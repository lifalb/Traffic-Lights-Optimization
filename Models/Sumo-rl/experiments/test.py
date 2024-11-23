from stable_baselines3.dqn.dqn import DQN
from sumo_rl import SumoEnvironment
import pandas as pd
import numpy as np
import os 


# 1- Define your SUMO net file .net.xml
net_file = os.path.join(os.pardir, os.pardir,os.pardir, "training_network", "osm.net.xml")

# 2- Define your folder path that contains the tests .rou.xml files
route_root_file = os.path.join(os.pardir, os.pardir,os.pardir, "tests")

# 3- Define your SUMO additional files
additional_files = os.path.join(os.pardir, os.pardir,os.pardir, "training_network", "osm.poly.xml.gz")

# 4- Define the route file of the output files (where you want to keep the output files)
output_csv_root_path = os.path.join(os.pardir,os.pardir, os.pardir, "outputs - test", "Sumo-rl/")

# 5- Define the  model path
model_path = os.path.join(os.pardir, os.pardir,os.pardir, "outputs - train/Sumo-rl/model/dqn_model")

# Number of simulation steps
total_time = 9600

# Number of tests
num_tests = 6

# Define the name of each .rou.xml file 
file_name = 'osm_test_'

for i in range(1, num_tests+1):
    route_file_name = f'{file_name}{i}.rou.xml'
    new_env = SumoEnvironment(
        net_file=net_file,
        route_file=f"{route_root_file}/{route_file_name}",  # route file for each test scenario
        out_csv_name=f"", #could be empty i dont need it
        single_agent=True,
        use_gui=True,
        num_seconds=total_time,  # You can set the total time for the test
        additional_files= additional_files # Additional files if any
    )

    # Load the pre-trained model
    model = DQN.load(model_path, env=new_env)
    output_csv_name = f"{output_csv_root_path}test_{i}.csv"
    # Run the model on the new environment
    obs, _ = new_env.reset()
    done = False
    truncated = False
    info_list = []
    while not (done or truncated):
        action, _states = model.predict(obs, deterministic=True)  # Get action from the model
        obs, reward, done,truncated, info = new_env.step(action)  # Take action in the new environment
        info_list.append(info)

    df = pd.DataFrame(info_list)
    # get the last step number
    step_number=info_list[len(info_list) - 1]['step']
    # get the evaluation metrics
    summed_values = df.sum(numeric_only=True).to_dict()
    summed_df = pd.DataFrame([summed_values])
    summed_df['accumulated_avg_wait_times'] = summed_df['accumulated_wait_times'] / summed_df['number_of_vehciles']
    summed_df['accumulated_pedestrian_avg_wait_times'] = np.where(
        summed_df['number_of_pedestrians'] > 0,
        summed_df['accumulated_pedestrian_wait_times'] / summed_df['number_of_pedestrians'],
        0 
    )
    summed_df['accumulated_average_fuel_consumption'] = summed_df['accumulated_total_fuel_consumption'] / summed_df['number_of_vehciles']
    summed_df['accumulated_avg_queue_length'] = summed_df['accumulated_queue_length'] / step_number
    new_env.close()  # Close the environment after the run
    summed_df.to_csv(output_csv_name)
