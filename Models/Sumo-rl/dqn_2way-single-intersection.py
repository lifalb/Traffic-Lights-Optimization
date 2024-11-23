import os
import sys

import gymnasium as gym
from stable_baselines3.dqn.dqn import DQN


if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")
import traci

from sumo_rl.env import SumoEnvironment


if __name__ == "__main__":
    # total time for each episode
    total_time = 9600

    # total time steps for all episodes 
    steps_per_episode = 9600
    num_episodes = 150/5
    total_timesteps = num_episodes * steps_per_episode
    
    # initialize environemnt 
    env = SumoEnvironment(
        net_file="sumo_rl/nets/abudhabi-intersection-train/osm.net.xml",
        route_file="sumo_rl/nets/abudhabi-intersection-train/osm-new.rou.xml",
        out_csv_name="outputs/abudhabi-intersection-train/dqn",
        single_agent=True,
        use_gui=False,
        num_seconds=total_time,
        additional_files= "sumo_rl/nets/abudhabi-intersection-train/osm.poly.xml.gz"
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
    model.learn(total_timesteps=total_timesteps)
    model.save("outputs/abudhabi-intersection/dqn_model")
