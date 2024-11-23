class TrafficGenerator:
    def __init__(self, num_of_seconds, output_file_name):
        self.num_of_seconds = num_of_seconds
        self.output_file_name = output_file_name.strip('"')

    def generate_routefile(self):
        """
        Generation of the route of every car for one episode
        """

        low = 0.01
        medium = 0.15
        high = 0.3
        cycles_probabilities_description = [[medium, medium, medium, medium], 
                                            [low, low, low, high],
                                            [low, low, high, low],
                                            [low, high, low, low],
                                            [high, low, low, low],
                                            [high, low, low, high],
                                            [low, high, high, low],
                                            [low, low, low, low]]
        # cycles_probabilities_description = [[low, low, low, low]]
        
        num_of_cycles = len(cycles_probabilities_description)
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
            # indicies of left turns to half the probabilty
            left_turns_idx = [1, 3, 4, 5, 10, 11, 12, 14]
            begin = 0
            for k in range(num_of_cycles):
                flow_description = cycles_probabilities_description[k]
                end = begin + duration_of_one_cycle
                for i in range(4):
                    for j in range(4):
                        index = i*4 + j
                        flow_val = flow_description[i]/2 if index in left_turns_idx else flow_description[i]
                        print(f'<flow id="type{i}{j}_{k}"   begin="{begin}" type="veh_passenger" route="route{i}{j}" departLane = "best" end="{end}" probability = "{flow_val}"/>',  file=routes)
                begin = end
            print("</routes>", file=routes)


# traffic_generator = TrafficGenerator(9600,'osm-new.rou.xml')
# traffic_generator.generate_routefile()