import traci
import pandas as pd
import os

# Define your SUMO configuration file (.sumocfg) path
sumo_config = os.path.join(os.pardir, os.pardir, "training_network", "osm-test.sumocfg")

# Define the tests file path (the file that includes the tests), it should be defined relative to the sumo_config - or define its path from the root
test_files_path = os.path.join(os.pardir, "tests/")

# Define the route file of the output files (where you want to keep the output files)
output_csv_root_path = os.path.join(os.pardir, os.pardir, "outputs - test", "BasicTLS/")

# Number of simulation steps
num_steps = 9600

# Number of tests
num_tests = 6

for i in range(1, num_tests+1):
    # Generate new sumo config for each new test as the route file changes
    config_content = f"""<?xml version="1.0" encoding="UTF-8"?>

<!-- generated on 2024-11-05 13:59:23 by Eclipse SUMO sumo Version 1.20.0
-->

<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">

    <input>
        <net-file value="osm.net.xml"/>
        <!-- <route-files value="osm.bus.trips.xml,osm.passenger.trips.xml,osm.pedestrian.rou.xml"/> -->
        <route-files value="{test_files_path}osm_test_{i}.rou.xml"/>
        <additional-files value="osm.poly.xml.gz"/>
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
        <gui-settings-file value="osm.view.xml"/>
    </gui_only>

</configuration>
"""
    # Write the configuration content to the file
    with open(sumo_config, 'w') as file:
        file.write(config_content)

    # output evaluation metrics path
    output_csv_path = f'{output_csv_root_path}test_{i}.csv'

    # start new connection with each test
    sumo_cmd = ["sumo", "-c", sumo_config]  
    traci.start(sumo_cmd)
    # metrics for this test
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

    traci.close()
    # calculate averages
    average_queue_length = total_queue_length / num_steps
    average_waiting_time = total_waiting_time / total_number_of_vehciles
    average_fuel_consumption = total_fuel_consumption / total_number_of_vehciles
    average_pedestrain_waiting_time=(total_pedestrian_waiting_time/total_number_of_pedestrians) if total_number_of_pedestrians > 0  else 0

    data = {
        'accumulated_wait_times': [total_waiting_time],
        'accumulated_avg_wait_times': [average_waiting_time],
        'accumulated_queue_length': [total_queue_length],
        'accumulated_avg_queue_length': [average_queue_length],
        'accumulated_total_fuel_consumption' : [total_fuel_consumption], 
        'accumulated_avg_fuel_consumption' : [average_fuel_consumption],
        'accumulated_pedestrian_wait_times':[total_pedestrian_waiting_time],
        'accumulated_pedestrian_avg_wait_times' : [average_pedestrain_waiting_time]
    }
    
    df = pd.DataFrame(data)
    df.to_csv(output_csv_path, index=False)
