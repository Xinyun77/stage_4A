import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import random as rd
import time
import json
import datetime
import matplotlib.dates as mdates

# function takes a dataframe as input
# removes mobilities that have no travel distance and returns a modified dataframe
def remove0Distance(df):
    """

    Args:
        df:

    Returns:

    """

    ID = df['ID'].tolist()
    indices = [i for i, x in enumerate(ID) if ID.count(x) > 1]
    dataframe = df.loc[indices]
    dataframe = dataframe.reset_index(drop=True)
    return dataframe

# function takes a dataframe of demand and the name of on-demand mobility service
# returns a dataframe containing only on-demand mobility service
def only_on_demand(df, on_demand_mobility):
    """

    Args:
        df:
        on_demand_mobility:

    Returns:

    """
    service = df.SERVICE.tolist()
    indices = [i for i, x in enumerate(service) if x == on_demand_mobility]
    dataframe = df.loc[indices]
    return dataframe

# function takes the path of the simulation output
# plot and save the evolution of vehicle state
def computeDynamic(dir):
    """

    Args:
        dir:

    Returns:

    """
    veh = pd.read_csv(dir + '/veh.csv', encoding='latin-1', delimiter=';')
    veh2 = remove0Distance(veh)
    table = veh2.groupby(['TIME', 'STATE']).ID.count().unstack().fillna(0)
    ax = table.plot.area()
    ax.tick_params(axis='x', labelrotation=45)
    plt.savefig(dir + '/graph/dynamic_veh.png', bbox_inches='tight')

# function calculates the number of trips realized by the vehicle
def nbTravels(index, df):
    """

    Args:
        index:
        df:

    Returns:

    """
    State = df.STATE.tolist()
    i_start = [index[0]]
    i_end = []
    step = []
    cpt = 0
    t = 0
    for t in range(len(index) - 1):
        if (State[index[t]] == 'STOP') & (t != len(index) - 1):  # if not the last stop
            i_start.append(index[t + 1])
            i_end.append(index[t])
            cpt += 1
            t = t
    if (State[index[-1]] == 'STOP'):  # if the last stop
        i_end.append(index[-1])
        cpt += 1
    return (cpt, i_start, i_end)

# function creates the dataframe containing vehicle's global indicators
def buildDataframe_global(time, dist, nbPass):
    """

    Args:
        time:
        dist:
        nbPass:

    Returns:

    """
    data = [['TIME', sum(time), mean(time), min(time), max(time), np.std(time)],
            ['DISTANCE', sum(dist), mean(dist), min(dist), max(dist), np.std(dist)],
            ['PASSENGERS', sum(nbPass), mean(nbPass), min(nbPass), max(nbPass), np.std(nbPass)]]
    df = pd.DataFrame(data, columns=['PARAMETRE', 'Total', 'Mean', 'Min', 'Max', 'Sd'])
    return df

# function creates the dataframe containing vehicle's individual indicators
def buildDataframe(ids, time, dist, nbPass):
    """

    Args:
        ids:
        time:
        dist:
        nbPass:

    Returns:

    """
    d = {'ID': ids, 'TIME': time, 'DISTANCE': dist, 'PASSENGERS': nbPass}
    df = pd.DataFrame(data=d)
    return df

# principal function which calculates and creates csv files containing both individual
# and global indicators
def computeStatic(dir):
    """

    Args:
        dir:

    Returns:

    """
    veh = pd.read_csv(dir + '/veh.csv', encoding='latin-1', delimiter=';')
    df = remove0Distance(veh)
    time = []
    dist = []
    nbPass = []
    ids = list(set(df.ID.tolist()))
    ID = df.ID.tolist()
    State = df.STATE.tolist()
    Distance = df.DISTANCE.tolist()
    Passenger = df.PASSENGERS.tolist()
    # cleanNan = lambda l : [x for x in l if str(x) != 'nan']  # clean nan
    Time = [float(i[:2]) * 3600 + float(i[3:5]) * 60 for i in df.TIME.tolist()]  # turn time to second
    for i in ids:
        index = [m for m, x in enumerate(ID) if (x == i)]
        nb, i_start, i_end = nbTravels(index, df)
        if nb != 0:
            travel_time = sum([Time[i_end[i]] - Time[i_start[i]] for i in range(len(i_start))])
            time.append(travel_time)
            dist.append(sum([Distance[i_end[i]] for i in range(len(i_end))]))
            nbPass.append(nb)
        else:  # no passengers, no travels
            time.append(0)
            dist.append(0)
            nbPass.append(0)
    df1 = buildDataframe(ids, time, dist, nbPass)
    df2 = buildDataframe_global(time, dist, nbPass)
    df1.to_csv('static_veh.csv', index=False, sep=';')  # static
    df2.to_csv('global_veh.csv', index=False, sep=';')  # global
    # distance per passenger
    sum_distance = df2.iloc[1]['Total']
    sum_passenger = df2.iloc[2]['Total']
    distance_per_passenger = (sum_distance / sum_passenger) * 1e-3  # km
    return distance_per_passenger

# function plot and save the speed evaluation of vehicles
def speed_evolution(dir):
    """

    Args:
        dir:

    Returns:

    """
    flow = pd.read_csv(dir + '/flow.csv', encoding='latin-1', delimiter=";")
    flow2 = flow[['TIME', 'SPEED']].groupby('TIME').mean().reset_index()
    speed = flow2.SPEED
    time = [i[:5] for i in flow2.TIME]
    times = [datetime.datetime.strptime(i, '%H:%M').time() for i in time]
    ax = plt.axes()
    # Convert datetime.time objects into datetime.datetime objects by adding a date
    # to the time
    datetimes = [datetime.datetime.combine(datetime.date.today(), t) for t in times]
    ax.plot(datetimes, speed, color='seagreen')
    ax.set_title('Speed evolution')
    ax.set_ylabel('Speed')
    ax.set_xlabel('Time')
    # Re-format the x-axis
    fmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_formatter(fmt)
    plt.savefig(dir + f"/graph/speed_evolution_veh")
    #plt.show()


if __name__ == '__main__':
    computeDynamic('OUTPUTS')  # dynamic indicators of vehicles
    computeStatic('OUTPUTS')   # static indicators of vehicles