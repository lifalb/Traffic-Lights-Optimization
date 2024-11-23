from __future__ import absolute_import
from __future__ import print_function
import os
from testing_simulation import Simulation
from generate import TrafficGenerator
from model import TestModel
from utils import import_test_configuration, set_sumo
import pandas as pd

#1- Define your SUMO configuration file (.sumocfg) path (without file name, define file name in testing_settings.ini)
sumo_config = os.path.join(os.pardir, os.pardir,os.pardir, "training_network")

#2- Define the tests file path (the file that includes the tests), it should be defined relative to the sumo_config - or define its path from the root
test_files_path = os.path.join(os.pardir, "tests/")

#3- Define the route file of the output files (where you want to keep the output files)
output_csv_root_path = os.path.join(os.pardir, os.pardir,os.pardir, "outputs - test", "Andrea/")

# Define the model path that you want to test
model_path = os.path.join(os.pardir, os.pardir,os.pardir, "outputs - train/Andrea/model/trained_model.h5")

# Number of simulation steps
num_steps = 9600

# Number of tests
num_tests = 6

if __name__ == "__main__":

    for i in range(1, num_tests+1):
        config_content = f"""<?xml version="1.0" encoding="UTF-8"?>

<!-- generated on 2024-11-05 13:59:23 by Eclipse SUMO sumo Version 1.20.0
-->

<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">

    <input>
        <net-file value="abudhabi-intersection-train/osm.net.xml"/>
        <!-- <route-files value="osm.bus.trips.xml,osm.passenger.trips.xml,osm.pedestrian.rou.xml"/> -->
        <route-files value="{test_files_path}osm_test_{i}.rou.xml"/>
        <additional-files value="abudhabi-intersection-train/osm.poly.xml.gz"/>
    </input>
    <processing>
        <ignore-route-errors value="true"/>
        <tls.actuated.jam-threshold value="30"/>
    </processing>

    <routing>
        <device.rerouting.adaptation-steps value="18"/>
        <device.rerouting.adaptation-interval value="10"/>
    </routing>

    <report>
        <verbose value="true"/>
        <duration-log.statistics value="true"/>
        <no-step-log value="true"/>
    </report>

    <gui_only>
        <gui-settings-file value="abudhabi-intersection-train/osm.view.xml"/>
    </gui_only>

</configuration>
"""
        config = import_test_configuration(config_file='testing_settings.ini')
        sumo_file_name = config['sumocfg_file_name']
        sumo_config_full_path = f'{sumo_config}/{sumo_file_name}'
        with open(sumo_config_full_path, 'w') as file:
            file.write(config_content)

        sumo_cmd = set_sumo(config['gui'], sumo_config ,config['sumocfg_file_name'], config['max_steps'])
        
        Model = TestModel(
            input_dim=config['num_states'],
            model_path=model_path
        )

        TrafficGen = TrafficGenerator(
            config['max_steps'], 
            config['n_cars_generated']
        )
        
        Simulation_obj = Simulation(
            Model,
            TrafficGen,
            sumo_cmd,
            config['max_steps'],
            config['green_duration'],
            config['yellow_duration'],
            config['num_states'],
            config['num_actions']
        )

        print('\n----- Test episode')
        simulation_time = Simulation_obj.run(config['episode_seed'])  # run the simulation
        print('Simulation time:', simulation_time, 's')


        data = {
            'accumulated_wait_times':Simulation_obj._accumulated_wait_times,
            'accumulated_avg_wait_times':Simulation_obj._accumulated_avg_wait_times,
            'accumulated_queue_length':Simulation_obj._accumulated_queue_length,
            'accumulated_avg_queue_length':Simulation_obj._accumulated_avg_queue_length,
            'accumulated_total_fuel_consumption':Simulation_obj._accumulated_total_fuel_consumption,
            'accumulated_avg_fuel_consumption':Simulation_obj._accumulated_avg_fuel_consumption,
            'accumulated_pedestrian_wait_times':Simulation_obj._accumulated_pedestrian_wait_times,
            'accumulated_pedestrian_avg_wait_times':Simulation_obj._accumulated_pedestrian_avg_wait_times,
        }
        df = pd.DataFrame(data)
        output_csv_path = f'{output_csv_root_path}test_{i}.csv'
        df.to_csv(output_csv_path, index=False)
