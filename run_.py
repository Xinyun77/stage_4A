import os

from mnms.mobility_service.on_demand import OnDemandDepotMobilityService
from mnms.simulation import Supervisor
from mnms.demand import CSVDemandManager
from mnms.flow.MFD import Reservoir, MFDFlowMotor
from mnms.log import attach_log_file, LOGLEVEL, get_logger, set_all_mnms_logger_level, set_mnms_logger_level
from mnms.time import Time, Dt
from mnms.io.graph import load_graph, load_odlayer
from mnms.travel_decision.logit import LogitDecisionModel
from mnms.tools.observer import CSVUserObserver, CSVVehicleObserver
from mnms.generation.layers import generate_bbox_origin_destination_layer
from mnms.mobility_service.personal_vehicle import PersonalMobilityService
from mnms.mobility_service.public_transport import PublicTransportMobilityService
from mnms.io.graph import save_transit_link_odlayer, load_transit_links

import pandas as pd
import random

indir = "INPUTS"
outdir = "OUTPUTS"

# set_all_mnms_logger_level(LOGLEVEL.WARNING)
set_mnms_logger_level(LOGLEVEL.INFO, ["mnms.simulation"])

# get_logger("mnms.graph.shortest_path").setLevel(LOGLEVEL.WARNING)
attach_log_file(outdir + '/simulation.log')


# 'DESTINATION_R_82604106' 'ORIGIN_E_83202447'

def calculate_V_MFD(acc):
    # V = 10.3*(1-N/57000) # data from fit prop
    V = 0  # data from fit dsty
    N = acc["CAR"]
    if N < 18000:
        V = 11.5 - N * 6 / 18000
    elif N < 55000:
        V = 11.5 - 6 - (N - 18000) * 4.5 / (55000 - 18000)
    elif N < 80000:
        V = 11.5 - 6 - 4.5 - (N - 55000) * 1 / (80000 - 55000)
    # V = 11.5*(1-N/60000)
    V = max(V, 0.001)  # min speed to avoid gridlock
    V_TRAM_BUS = 0.7 * V
    # return {"CAR": V, "METRO": 17, "BUS": V_TRAM_BUS, "TRAM": V_TRAM_BUS}
    return {"CAR": V}


def entry_exit_ODlayer(emps_path, nx, ny, graph):
    emps = pd.read_csv(emps_path, encoding='latin-1', delimiter=';')
    odlayer_crea = generate_bbox_origin_destination_layer(graph.roads, nx, ny)
    for i in emps.index:
        if emps.Type[i] == "Entry":
            origin_name = "Origin_Car_node_" + emps.ID[i]
            odlayer_crea.create_origin_node(origin_name, list(map(float, str(emps.geometry[i])[7:-1].split())))
        else:
            destination_name = "Destination_Car_node_" + emps.ID[i]
            odlayer_crea.create_destination_node(destination_name,
                                                 list(map(float, str(emps.geometry[i])[7:-1].split())))
    return odlayer_crea


def percentage_uber(p, demande):
    ID = demande['ID'].tolist()
    departure = demande['DEPARTURE'].tolist()
    origin = demande['ORIGIN'].tolist()
    destination = demande['DESTINATION'].tolist()
    service = demande['SERVICE'].tolist()
    l = list(range(len(demande)))
    indices = random.sample(l, int(p*len(demande)))
    for i in indices:
        service[i] = "UBER"
    tmp = list(zip(ID, departure, origin, destination, service))
    df = pd.DataFrame(tmp, columns = ['ID', 'DEPARTURE', 'ORIGIN', 'DESTINATION', 'SERVICE'])
    return df


if __name__ == '__main__':
    NX = 14
    NY = 16
    DIST_CONNECTION = 1000

    mmgraph = load_graph(indir + "/new_network.json")
    odlayer = generate_bbox_origin_destination_layer(mmgraph.roads, NX, NY)

    mmgraph.add_origin_destination_layer(odlayer)

    # save_odlayer(odlayer,  indir + f"/odlayer_lyon.json")

    # od_layer2 = load_odlayer(indir + f"/odlayer_lyon.json")

    if not os.path.exists(indir + f"/transit_link_{NX}_{NY}_{DIST_CONNECTION}_grid.json"):
        mmgraph.connect_origin_destination_layer(DIST_CONNECTION)
        save_transit_link_odlayer(mmgraph, indir + f"/transit_link_{NX}_{NY}_{DIST_CONNECTION}_grid.json")
    else:
        load_transit_links(mmgraph, indir + f"/transit_link_{NX}_{NY}_{DIST_CONNECTION}_grid.json")

    personal_car = PersonalMobilityService()
    personal_car.attach_vehicle_observer(CSVVehicleObserver(outdir + "/veh.csv"))
    mmgraph.layers["CAR"].add_mobility_service(personal_car)

    # bus_service = PublicTransportMobilityService("BUS")
    # bus_service.attach_vehicle_observer(CSVVehicleObserver(outdir + "/veh.csv"))
    # mmgraph.layers["BUSLayer"].add_mobility_service(bus_service)

    # tram_service = PublicTransportMobilityService("TRAM")
    # tram_service.attach_vehicle_observer(CSVVehicleObserver(outdir + "/veh.csv"))
    # mmgraph.layers["TRAMLayer"].add_mobility_service(tram_service)

    # metro_service = PublicTransportMobilityService("METRO")
    # metro_service.attach_vehicle_observer(CSVVehicleObserver(outdir + "/veh.csv"))
    # mmgraph.layers["METROLayer"].add_mobility_service(metro_service)

    # creation service de mobilité:
    uber = OnDemandDepotMobilityService("UBER", 0)
    uber.attach_vehicle_observer(CSVVehicleObserver("veh.csv"))
    mmgraph.layers["CAR"].add_mobility_service(uber)

    # -------------- Add depots ---------------

    #uber.add_depot("m1003028151", capacity=5)  #  52.36296620235635, 4.804315400116319   44% uber have benn found
    #uber.add_depot("m1014426667", capacity=5)
    uber.add_depot("m1016716190", capacity=5)  #  52.39025250329249, 4.8849803001694525
    #uber.add_depot("m1029631236", capacity=5)  #  52.384873203248524, 4.881513100166867

    print("Input file \n")
    # --------------- Input file with a percenatge of uber -------------------
    demand_file = indir + "/test_uber1.csv"          # Input demand csv
    demand_data = pd.read_csv(demand_file, delimiter=';')
    demand_with_uber = percentage_uber(0.1, demand_data)  # with a percentage of uber
    demand_with_uber.to_csv(indir + "/test_uber_.csv", sep=';', index=False)
    demand_file_name = indir + "/test_uber_.csv"      # demand with UBER

    demand = CSVDemandManager(demand_file_name)
    demand.add_user_observer(CSVUserObserver(outdir + "/user.csv"), user_ids="all")

    flow_motor = MFDFlowMotor(outfile=outdir + "/flow.csv")
    # flow_motor.add_reservoir(Reservoir(mmgraph.roads.zones["RES"], ["CAR", "BUS"], calculate_V_MFD))
    flow_motor.add_reservoir(Reservoir(mmgraph.roads.zones["RES"], ["CAR"], calculate_V_MFD))

    travel_decision = LogitDecisionModel(mmgraph, outfile=outdir + "/path.csv")

    supervisor = Supervisor(graph=mmgraph,
                            flow_motor=flow_motor,
                            demand=demand,
                            decision_model=travel_decision,
                            outfile=outdir + "/travel_time_link.csv")

    supervisor.run(Time('07:00:00'), Time('07:40:00'), Dt(minutes=1), 10)
