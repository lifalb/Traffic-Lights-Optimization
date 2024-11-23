import os
import sys

import gymnasium as gym
from stable_baselines3.dqn.dqn import DQN
import time

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

from sumo_rl import SumoEnvironment

# 1- Define your SUMO net file .net.xml
net_file = os.path.join(os.pardir, os.pardir,os.pardir, "training_network", "osm.net.xml")

# 2- Define your SUMO route file .rou.xml
route_file = os.path.join(os.pardir, os.pardir,os.pardir, "training_network", "osm-new.rou.xml")

# 3- Define your SUMO additional files
additional_files = os.path.join(os.pardir, os.pardir,os.pardir, "training_network", "osm.poly.xml.gz")

# 4- Define the route file of the output files (where you want to keep the output files)
output_csv_root_path = os.path.join(os.pardir, os.pardir, os.pardir, "outputs - train", "Sumo-rl/")

# 5- Define th output path of the model (make sure to change the path of the folder according to what parameter you are changing)
model_output_path=os.path.join(os.pardir, os.pardir,os.pardir, "outputs - ablation", "reward/dqn_model")

if __name__ == "__main__":
    # total time (steps) for simulation per episode
    total_time = 9600

    # number of episodes (should be divided by 5)
    num_episodes = 150/5

    # total time steps with episodes for the model to learn on
    total_timesteps = num_episodes * total_time
    
    env = SumoEnvironment(
        net_file=net_file,
        route_file=route_file,
        out_csv_name=output_csv_root_path,
        single_agent=True,
        use_gui=False,
        num_seconds=total_time,
        additional_files= additional_files
    )

    model = DQN(
        env=env,
        policy="MlpPolicy",
        learning_rate=0.001,
        learning_starts=0,
        train_freq=1,
        target_update_interval=500,
        exploration_initial_eps=0.05,
        exploration_final_eps=0.01,
        verbose=1,
    )
    start = time.time()
    model.learn(total_timesteps=total_timesteps)
    model.save(model_output_path)
    print('TOTAL TIME: ', time.time() - start)
