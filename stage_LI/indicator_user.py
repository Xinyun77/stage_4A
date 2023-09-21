
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import random as rd
import time
import json
import datetime
import matplotlib.dates as mdates

"""
Static indicators (individual and global)
- by Xinyun
"""
# function calculates the number of vehicles borrowed by users
def nbVehicles(index, df):

    """

    Args:
        index:
        df:

    Returns:

    """
    State = df.STATE.tolist()
    veh = df.VEHICLE.tolist()
    i_start = [index[0]]
    i_end = []
    step = []
    t = 0
    for t in range(len(index) - 1):
        if (State[index[t]] == 'ARRIVED') & (t != len(index) - 1): # if not the last stop
            i_start.append(index[t+1])
            i_end.append(index[t])
            t = t
    i_end.append(index[-1])
    v = [veh[i] for i in index]
    tmp = [x for x in v if str(x) != "nan"]
    cpt = len(list(set(tmp)))
    return (cpt, i_start, i_end)

# function creates the dataframe containing user's global indicators
def buildDataframe_global_user(time, dist, nbVeh):
    """

    Args:
        time:
        dist:
        nbVeh:

    Returns:

    """
    data = [['TIME', sum(time), mean(time), min(time), max(time), np.std(time)],
            ['DISTANCE', sum(dist), mean(dist), min(dist), max(dist), np.std(dist)],
             ['VEHICLE', sum(nbVeh), mean(nbVeh), min(nbVeh), max(nbVeh), np.std(nbVeh)]]
    df = pd.DataFrame(data, columns=['PARAMETRE', 'Total', 'Mean', 'Min', 'Max', 'Sd'])
    return df

# function creates the dataframe containing user's individual indicators
def buildDataframeUser(ids, time, dist, nbVeh):
    """

    Args:
        ids:
        time:
        dist:
        nbVeh:

    Returns:

    """
    d = {'ID': ids, 'TIME': time, 'DISTANCE': dist, 'VEHICLE': nbVeh}
    df = pd.DataFrame(data = d)
    return df

# principal function which calculates and creates csv files containing both individual
# and global indicators
def computeStaticUser(dir):
    """

    Args:
        dir:

    Returns:

    """
    df = pd.read_csv(dir + '/user.csv', encoding='latin-1', delimiter=';')
    time = []
    dist = []
    nbVeh = []
    ids = list(set(df.ID.tolist()))
    ID = df.ID.tolist()
    State = df.STATE.tolist()
    Distance = df.DISTANCE.tolist()
    veh = df.VEHICLE.tolist()
    Time = [float(i[:2])*3600 + float(i[3:5])*60 for i in df.TIME.tolist()]  # turn to second
    for i in ids:
        index = [m for m,x in enumerate(ID) if (x == i)]
        nb, i_start, i_end = nbVehicles(index, df)
        if nb != 0:
            travel_time = sum([Time[i_end[j]] - Time[i_start[j]] for j in range(len(i_start))])
            time.append(travel_time)
            dist.append(sum([Distance[i_end[j]] for j in range(len(i_end))]))
            nbVeh.append(nb)
        else:  # no passengers, no travels
            time.append(0)
            dist.append(0)
            nbVeh.append(0)
    ids = [ids[i] for i, x in enumerate(dist) if x != 0]   # dist != 0
    time = [time[i] for i, x in enumerate(dist) if x != 0]
    nbVeh = [nbVeh[i] for i, x in enumerate(dist) if x != 0]
    dist = [x for x in dist if x!= 0]
    df1 = buildDataframeUser(ids, time, dist, nbVeh)
    df2 = buildDataframe_global_user(time, dist, nbVeh)
    df1.to_csv(dir + '/user_static.csv', index=False, sep=';')
    df2.to_csv(dir + '/user_global.csv', index=False, sep=';')

## ----------------------------------------------------------------------- ##

"""
dynamic indicators
- by Oscar
"""

def waiting_time(df_w, list_w):
    """

    @param df_w:
    @param list_w:
    @return:
    """
    w = 0
    waiting_answer = df_w[df_w.STATE == 'WAITING_ANSWER']
    if not waiting_answer.empty:
        h1 = waiting_answer[0]
        h2 = waiting_answer[-1]
        h1h2 = float(h2[0:2]) * 3600 + float(h2[3:5]) * 60 + float(h2[6:8]) - float(h1[0:2]) * 3600 + float(
            h1[3:5]) * 60 + float(h1[6:8])
        w += h1h2
    waiting_vehicle = df_w[df_w.STATE == 'WAITING_VEHICLE']
    if not waiting_vehicle.empty:
        h1 = waiting_vehicle[0]
        h2 = waiting_vehicle[-1]
        h1h2 = float(h2[0:2]) * 3600 + float(h2[3:5]) * 60 + float(h2[6:8]) - float(h1[0:2]) * 3600 + float(
            h1[3:5]) * 60 + float(h1[6:8])
        w += h1h2
    list_w.append(w)

def graph_data(df, dir):
    """

    @param df:
    @param dir:
    @return:
    """
    df_arrived = df[df.Arrived]
    plt.hist(df_arrived.Time)
    plt.xlabel('Time (s)')
    plt.ylabel('User')
    plt.axvline(df_arrived.Time.mean(), color='red')
    plt.axvline(df_arrived.Time.median(), color='yellow')
    plt.savefig(dir + f"/graph/time")
    plt.close()

    plt.hist(df_arrived.Distance)
    plt.xlabel('Distance (m)')
    plt.ylabel('User')
    plt.axvline(df_arrived.Distance.mean(), color='red')
    plt.axvline(df_arrived.Distance.median(), color='yellow')
    plt.savefig(dir + f"/graph/distance")
    plt.close()

def data_transformation(df_user):
    """

    @param df_user:
    @return:
    """
    u = df_user
    u = u.groupby('ID').apply(walking_sim)
    u.reset_index(drop=True, inplace=True)
    u = u.sort_values('TIME')
    u.reset_index(drop=True, inplace=True)
    u = u.groupby('ID').apply(get_main_activity)
    u.reset_index(drop=True, inplace=True)
    u = u.sort_values('TIME')
    u.reset_index(drop=True, inplace=True)

    return u

def time_round(str_time):
    """
    @param str_time:
    @return:
    """
    return str_time[-5:] == '00.00'

def arrived_sim(df):
    u = df

def walking_sim(df):
    u = df
    u_tampon = pd.DataFrame(data={'TIME': [], 'ID': [], 'LINK': [],
                                  'POSITION': [],
                                  'DISTANCE': [], 'STATE': [],
                                  'VEHICLE': [], 'CONTINUOUS_JOURNEY': []})
    for i in u[u.STATE == 'WALKING'].index:
        time_delta = pd.to_timedelta(u.loc[i].TIME) + pd.to_timedelta('00:01:00')
        time_delta_max = pd.to_timedelta(u.loc[u.index[list(u.index).index(i) + 1]].TIME)
        while time_delta < time_delta_max:
            u2 = pd.DataFrame(
                data={'TIME': [str(time_delta)[7:12] + ':00.00'], 'ID': [u.loc[i].ID], 'LINK': [u.loc[i].LINK],
                      'POSITION': [u.loc[i].POSITION],
                      'DISTANCE': [u.loc[i].DISTANCE], 'STATE': [u.loc[i].STATE],
                      'VEHICLE': [u.loc[i].VEHICLE], 'CONTINUOUS_JOURNEY': [u.loc[i].CONTINUOUS_JOURNEY]})
            u_tampon = pd.concat([u_tampon, u2], ignore_index=True)
            time_delta += pd.to_timedelta('00:01:00')
    u = pd.concat([u, u_tampon], ignore_index=True)
    u = u.sort_values('TIME')
    u.reset_index(drop=True, inplace=True)
    return u

def get_main_activity(df):
    u = df
    l = list(u.TIME.apply(lambda x: pd.to_timedelta(x)).diff())[1:]
    l.append(pd.to_timedelta('00:00:00'))
    u['Time_delta'] = l
    u['TIME'] = u['TIME'].apply(lambda x: x[:5] + ':00.00')
    l_arrived = list(u['TIME'].loc[u.index[:-1]])
    l_arrived.append(str(pd.to_timedelta(u.loc[u.index[-1]].TIME) + pd.to_timedelta('00:01:00'))[7:12] + ':00.00')
    u['TIME'] = l_arrived
    u = u.groupby('TIME').apply(max_activity)
    u.reset_index(drop=True, inplace=True)
    return u

def max_activity(u_test):
    return u_test[u_test.Time_delta == u_test.Time_delta.max()]

def data_output_dynamic(dir):
    """

    @param dir:
    @return:
    """
    u = pd.read_csv(dir + '/user.csv', encoding='latin-1', delimiter=';')
    v = pd.read_csv(dir + '/veh.csv', encoding='latin-1', delimiter=';')
    u_transform = data_transformation(u)
    time_min = u_transform[u_transform.STATE == 'ARRIVED'].TIME.min()
    time_max = u_transform.TIME.max()
    u_tampon = u_transform.copy()
    while time_min < time_max:
        u2 = u_tampon[(u_tampon.TIME == time_min) & (u_tampon.STATE == 'ARRIVED')].copy()
        time_min = str(pd.to_timedelta(time_min) + pd.to_timedelta('00:01:00'))[7:12] + ':00.00'
        u2['TIME'] = u2['TIME'].apply(lambda x: time_min)
        u_tampon = pd.concat([u_tampon, u2], ignore_index=True)

    u_tampon = u_tampon.sort_values('TIME')
    u_tampon.reset_index(drop=True, inplace=True)
    u_output = u_tampon[u_tampon.TIME.apply(lambda x: x[-5:] == '00.00')].groupby(
        ['TIME', 'STATE']).count().ID.unstack().fillna(0)
    u_output.to_csv(dir + '/test_output_dynamic_data_state.csv', index=False, sep=';')
    graph = u_output.plot.area()
    graph.figure.savefig(dir + '/graph/State_time.pdf')
    list_str = v.PASSENGERS.fillna('')
    list_len = []
    for i in list_str:
        list_len.append(len(str(i).split()))
    v_transform = v
    v_transform['nb_Passengers'] = list_len
    v_output = v_transform[v_transform.TIME.apply(lambda x: x[-5:] == '00.00')][
        ['TIME', 'TYPE', 'nb_Passengers']].groupby(['TIME', 'TYPE']).sum().nb_Passengers.unstack().fillna(0)
    v_output.to_csv(dir + '/test_output_dynamic_data_type.csv', index=False, sep=';')
    graph = v_output.plot.area()
    graph.figure.savefig(dir + '/graph/Type_time.pdf')


if __name__ == '__main__':
    computeStaticUser('OUTPUTS')  # static indicators of uers
    data_output_dynamic('OUTPUTS')  #dynamic indicators of users