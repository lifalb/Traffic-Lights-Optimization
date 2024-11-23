import os

class TrafficGenerator:
    def __init__(self, num_of_seconds, output_file_name, cycles_probabilities_description, person_probabilty):
        self.num_of_seconds = num_of_seconds
        self.output_file_name = output_file_name
        self.cycles_probabilities_description = cycles_probabilities_description
        self.person_probabilty = person_probabilty
    def generate_routefile(self):
        """
        Generation of the route of every car for one episode
        """ 
        num_of_cycles = len(self.cycles_probabilities_description)
        duration_of_one_cycle = self.num_of_seconds // (num_of_cycles)
        print("duration_of_one_cycle: ", duration_of_one_cycle)
        # produce the file for cars generation, one car per line
        with open(self.output_file_name, "w") as routes:
            print("""<?xml version="1.0" encoding="UTF-8"?>


<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
    <!-- <route id="route00" color="1,1,0" edges="182191279#0 182191279#1 463663572#2"/> -->
    <route id="route00" color="1,1,0" edges="S2JE J2E"/>
    <!-- <route id="route01" color="1,1,0" edges="479203919#0 TL2S"/> -->
    <route id="route01" color="1,1,0" edges="S2TL TL2S"/>
    <!-- <route id="route02" color="1,1,0" edges="479203919#0 TL2N 1148455774#2"/> -->
     <route id="route02" color="1,1,0" edges="S2TL TL2N"/>
    <route id="route03" color="1,1,0" edges="S2TL TL2W"/>

    <!-- <route id="route10" color="1,1,0" edges="167719753#0 167719753#1 463663572#1"/> -->
     <route id="route10" color="1,1,0" edges="E2TL TL2E"/>
    <route id="route11" color="1,1,0" edges="E2TL TL2S"/>
    <route id="route12" color="1,1,0" edges="E2JN J2N"/>
    <route id="route13" color="1,1,0" edges="E2TL TL2W"/>

    <route id="route20" color="1,1,0" edges="W2TL TL2E"/>
    <route id="route21" color="1,1,0" edges="W2JS J2DS"/>
    <route id="route22" color="1,1,0" edges="W2TL TL2N"/>
    <route id="route23" color="1,1,0" edges="W2TL TL2W"/>

    <route id="route30" color="1,1,0" edges="N2TL TL2E"/>
    <route id="route31" color="1,1,0" edges="N2TL TL2S"/>
    <route id="route32" color="1,1,0" edges="N2TL TL2N"/>
    <route id="route33" color="1,1,0" edges="N2JW N2DW"/>
    <vType id="veh_passenger" vClass="passenger" maxSpeed = '70' color="1,0,0"/>
                  """, file=routes)

            print(f"""        <vType id="ped_pedestrian" vClass="pedestrian"/>
    <personFlow id="p0" begin="0" end="{self.num_of_seconds}" probability="{self.person_probabilty}">
        <walk edges=" PED_1 PED_2"/>
   </personFlow>
   <personFlow id="p1" begin="0" end="{self.num_of_seconds}" probability="{self.person_probabilty}">
        <walk edges="PED_3 PED_4"/>
   </personFlow>
   <personFlow id="p2" begin="0" end="{self.num_of_seconds}" probability="{self.person_probabilty}">
        <walk edges="PED_5 PED_6"/>
   </personFlow>
   <personFlow id="p3" begin="0" end="{self.num_of_seconds}" probability="{self.person_probabilty}">
        <walk edges="PED_7 PED_8"/>   </personFlow>
                  """, file=routes)
            # indicies of left turns to half the probabilty
            left_turns_idx = [1, 3, 4, 5, 10, 11, 12, 14]
            begin = 0
            for k in range(num_of_cycles):
                flow_description = self.cycles_probabilities_description[k]
                end = begin + duration_of_one_cycle
                for i in range(4):
                    for j in range(4):
                        index = i*4 + j
                        flow_val = flow_description[i]/2 if index in left_turns_idx else flow_description[i]
                        print(f'<flow id="type{i}{j}_{k}"   begin="{begin}" type="veh_passenger" route="route{i}{j}" departLane = "best" end="{end}" probability = "{flow_val}"/>',  file=routes)
                begin = end
            print("</routes>", file=routes)


# 1- Describe low, medium, high traffic scenario probabilties

low = 0.01
medium = 0.15
high = 0.3

# 2- Describe the traffic flow for each lane for each test

tests = [[[medium, medium, medium, medium]],
        [[medium, low, low, low]],
        [[low, medium, low, low]],
        [[low, low, medium, low]],
        [[low, low, low, medium]],
        [[high, high, high, high]]]

# 3- Describe the person flow with defining its probabilty to spawn at each second at each lane
person_probabilty = 0.05

# 4- Define the output folder path for the test .rou.xml files
output_root_folder = test_files_path = os.path.join(os.pardir, "tests/")

# 5- Define simulation time 
simulation_time = 9600

for idx, cycles_probabilities_description in enumerate(tests):
    traffic_generator = TrafficGenerator(simulation_time,f'{output_root_folder}/osm_test_{idx+1}.rou.xml', cycles_probabilities_description, person_probabilty)
    traffic_generator.generate_routefile()