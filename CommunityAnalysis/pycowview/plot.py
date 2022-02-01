###############################################################################
####                               PLOTS                                  #####
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from random import randint
import math
import matplotlib.lines as mlines
import matplotlib.patches as pat
from matplotlib.animation import FuncAnimation
from matplotlib import transforms
from datetime import datetime

from .extras import positions, positions_PA

# function to plot the outline of the barn
def plot_barn(filename):
        df = pd.read_csv(filename, skiprows = 0, sep = ';', header=0)
        df.columns = ['Unit', 'x1', 'x2', 'x3', 'x4', 'y1', 'y2', 'y3','y4']
        units = list(df['Unit'])
        x_1 = list(df['x1'])
        x_2 = list(df['x2'])
        x_3 = list(df['x3'])
        x_4 = list(df['x4'])
        y_1 = list(df['y1'])
        y_2 = list(df['y2'])
        y_3 = list(df['y3'])
        y_4 = list(df['y4'])

        fig, ax = plt.subplots(1,figsize=(6,6))
        for i in range(len(units)):
           art =  pat.Rectangle((x_1[i],min(y_1[i],y_2[i])),x_3[i]-x_1[i], max(y_1[i],y_2[i])-min(y_1[i],y_2[i]), fill = False)
           ax.add_patch(art)
           #print(ax.patches)
        ax.set_xlim(x_1[0]-2000,x_3[0]+2000)
        ax.set_ylim(y_1[0]-2000,y_2[0]+2000)
        return fig, ax
    
def plot_barnV2(filename):
        df = pd.read_csv(filename, skiprows = 0, sep = ';', header=0)
        df.columns = ['Unit', 'x1', 'x2', 'x3', 'x4', 'y1', 'y2', 'y3','y4']
        units = list(df['Unit'])
        x_1 = list(df['x1'])
        x_2 = list(df['x2'])
        x_3 = list(df['x3'])
        x_4 = list(df['x4'])
        y_1 = list(df['y1'])
        y_2 = list(df['y2'])
        y_3 = list(df['y3'])
        y_4 = list(df['y4'])

        fig, ax = plt.subplots(1,figsize=(8,5))
        for i in range(len(units)):
           art =  pat.Rectangle((y_2[i],max(x_2[i],x_3[i])),y_4[i]-y_2[i], min(x_2[i],x_3[i])-max(x_2[i],x_3[i]), fill = False)
           ax.add_patch(art)
           #print(ax.patches)
        ax.set_xlim(x_1[0]-2000,x_3[0]+2000)
        ax.set_ylim(y_1[0]-2000,y_2[0]+2000)
        return fig, ax

def plot_all_cows(ax, df_FA, time, exceptions):
    id_to_plot = []
    row_to_plot = []
    special_cows_id = []
    special_cows_index = []
    count = 0
    incident_position = []

    cow_1 = df_FA.loc[df_FA['tag_id'] == exceptions[0]]

    row_exception = cow_1.loc[cow_1['time'] == time]

    posx = row_exception['x'].values[0]
    posy = row_exception['y'].values[0]


    for index, row in df_FA.iterrows(): #for all rows in the data,
        if abs(row['time']-time)<10000 and row['tag_id'] not in id_to_plot and row['tag_id'] not in exceptions: #if they are within 10 seconds before or after and not already found or one of the interesting cows
            id_to_plot.append(row['tag_id'])
            row_to_plot.append(count)
            if 10000000>abs(row[4]-posx) and 1000000>abs(row[5]-posy): #if they are within
                special_cows_id.append(row['tag_id'])
                special_cows_index.append(count)
        count += 1

    cows_to_plot = df_FA.iloc[row_to_plot]

    return ax, special_cows_id


# function to plot the position of a cow (based on tag_id) for FA-data
def plot_cow(df, tag_id, filename_barn):
    fig, ax = plot_barn(filename_barn)
    if hasattr(tag_id, "__len__"):
        for i in tag_id:
            temp = df.loc[df['tag_id'] == i]
            x,y,z = positions(temp)
            plt.plot(x,y,'o--', markersize = 2)
    else:
        temp = df.loc[df['tag_id'] == tag_id]
        x,y,z = positions(temp)
        plt.plot(x,y,'o--', markersize = 2)
    plt.show()
   
# function to plot the distance between two cows
def plot_distance(df, tag_id1, tag_id2):
    cow_1 = df.loc[df['tag_id'] == tag_id1]
    cow_2 = df.loc[df['tag_id'] == tag_id2]
    x1,y1,z1 = positions(cow_1)
    x2,y2,z2 = positions(cow_2)
    
    times_1 = list(cow_1['time'])
    times_2 = list(cow_2['time'])
    
    distance_x = []
    distance_y = []
    
    distance_x.append(x1[0] - x2[0]) # initial distance
    distance_y.append(y1[0] - y2[0])
    i = 0 # index of times_1/x1/y1
    j = 0 # index of times_2/x2/y2
    times_comb = []
    times_comb.append(min(times_1[0], times_2[0]))
    while i < len(times_1)-1 or j < len(times_2)-1:
        if times_1[i] <= times_2[j]:           
            if i == len(times_1)-1:# if at end of times_1
                j = j+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2[j],times_1[i]))
            else:
                i = i+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2[j],times_1[i]))
        else:
            if j == len(times_2)-1: # if at end of times_2
                i = i+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2[j],times_1[i]))
            else:
                j = j+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2[j],times_1[i]))

    distance = []
    temp = times_comb[0]
    times_comb = [x - temp for x in times_comb] # set initial time to zero
    times_comb_plot = [x*1/(3600*1000) for x in times_comb] 

    for i in range(len(distance_x)):
        distance.append(math.sqrt(distance_x[i]**2 + distance_y[i]**2))
    fig, ax =  plt.subplots(1,figsize=(6,6))
    ax.plot(times_comb_plot, distance)
    ax.set_title('Distance between cow ' + str(tag_id1) + ' and ' + str(tag_id2))
    plt.show()
    hist_arr = np.zeros(times_comb[-1])
    index = 0
    for i in range(len(times_comb)-1):
        hist_arr[index:times_comb[i+1]] = distance[i]
        index = times_comb[i+1]

    plt.hist(hist_arr, bins=50)
    plt.show()
    
def plot_cow_PAv2(df, tag_id, filename_barn):
    fig, ax = plot_barn(filename_barn)
    temp = df.loc[df['tag_id'] == tag_id]
    x, y, z, activity = positions_PA(temp)
    current_activity = activity[0]
    for i in range(len(activity)):
        if activity[i] != current_activity:
            plt.plot(x[i], y[i], 'o--', markersize=2, color='k')

def plot_cow_PA(df, tag_id, filename_barn):
    fig, ax = plot_barn(filename_barn)
    if hasattr(tag_id, "__len__"):
        for id in tag_id:
            temp = df.loc[df['tag_id'] == id]
            x, y, z, activity = positions_PA(temp)
            for i in range(len(activity)):
                if activity[i] == 0:
                    plt.plot(x[i], y[i], 'o--', markersize=2, color='k')
                elif activity[i] == 1:
                    plt.plot(x[i], y[i], 'o--', markersize=2, color='b')
                elif activity[i] == 2:
                    plt.plot(x[i], y[i], 'o--', markersize=2, color='y')
                elif activity[i] == 3:
                    plt.plot(x[i], y[i], 'o--', markersize=2, color='r')
                elif activity[i] == 4:
                    plt.plot(x[i], y[i], 'o--', markersize=2, color='g')
                elif activity[i] == 5:
                    plt.plot(x[i], y[i], 'o--', markersize=2, color='m')
                else:
                    plt.plot(x[i], y[i], 'o--', markersize=2, color='c')
    else:
        temp = df.loc[df['tag_id'] == tag_id]
        x, y, z, activity = positions_PA(temp)
        for i in range(len(activity)):
            if activity[i] == 0:
                plt.plot(x[i], y[i], 'o--', markersize=2, color='k')
            elif activity[i] == 1:
                plt.plot(x[i], y[i], 'o--', markersize=2, color='b')
            elif activity[i] == 2:
                plt.plot(x[i], y[i], 'o--', markersize=2, color='y')
            elif activity[i] == 3:
                plt.plot(x[i], y[i], 'o--', markersize=2, color='r')
            elif activity[i] == 4:
                plt.plot(x[i], y[i], 'o--', markersize=2, color='g')
            elif activity[i] == 5:
                plt.plot(x[i], y[i], 'o--', markersize=2, color='m')
            else:
                plt.plot(x[i], y[i], 'o--', markersize=2, color='c')


    Blue = mlines.Line2D([], [], color='b', marker='.',
                            markersize=15, label='Standing')
    Yellow = mlines.Line2D([], [], color='y', marker='.',
                         markersize=15, label='Walking')
    Red = mlines.Line2D([], [], color='r', marker='.',
                           markersize=15, label='In cubicle')
    Green = mlines.Line2D([], [], color='g', marker='.',
                           markersize=15, label='At feed')
    Magenta = mlines.Line2D([], [], color='m', marker='.',
                           markersize=15, label='At drinker')
    Cyan = mlines.Line2D([], [], color='c', marker='.',
                           markersize=15, label='Outside')
    Black = mlines.Line2D([], [], color='k', marker='.',
                          markersize=15, label='Unknown')
    plt.legend(handles=[Blue, Yellow, Red, Green, Magenta, Cyan, Black])

    plt.show()



# function to plot all cows in a time interval
def plot_time(df, t1, t2):
    temp = df.loc[df['time'] <= t2]
    temp = temp.loc[df['time'] >= t1]
    x,y,z = positions(temp)
    plt.scatter(x,y, s = 2)
    plt.show()
        

# function to plot cows based on PC-data    
def plot_cow_PC(df, tag_id, filename_barn):       
    fig, ax = plot_barn(filename_barn)
    if hasattr(tag_id, "__len__"):
        colors = []
        for i in range(len(tag_id)):
            colors.append('#%06X' % randint(0, 0xFFFFFF))
                          
        zip_object_tag_col = zip(tag_id, colors)
        for i,c in zip_object_tag_col:
            temp = df.loc[df['tag_id'] == i]
            list_t1 = list(temp['end'])
            list_t2 = list(temp['start'])
            duration = []    
            zip_object = zip(list_t1, list_t2)
            for list1_i, list2_i in zip_object:
                duration.append(list1_i-list2_i)
            max_dur = max(duration)
            x,y,z = positions(temp)
            zip_object_pos = zip(x, y, duration)
            for xi,yi,di in zip_object_pos:
                size = 2
                if di > 2/4*max_dur:
                    size = size*3
                elif di  > 1/4*max_dur:
                    size = size*2
                elif di == 0:
                    size = 1
                plt.plot(xi,yi, color = c, marker='o', markersize = size)
    else:
        temp = df.loc[df['tag_id'] == tag_id]
        list_t1 = list(temp['end'])
        list_t2 = list(temp['start'])
        duration = [] 
        zip_object = zip(list_t1, list_t2)
        for list1_i, list2_i in zip_object:
            duration.append(list1_i-list2_i)
        max_dur = max(duration)
        x,y,z = positions(temp)
        zip_object_pos = zip(x, y, duration)
        for xi,yi,di in zip_object_pos:
            size = 2
            if di > 2/4*max_dur:
                size = size*3
            elif di  > 1/4*max_dur:
                size = size*2 
            elif di == 0:
                size = 1
            plt.plot(xi,yi,'bo--', markersize = size)
     
    plt.show()

# function to plot data from PAA-data    
def plot_cow_PAA(df, tag_id):
    temp = df.loc[df['tag_id'] == tag_id]
    act = list(temp['activity_type'])
    dur = list(temp['duration'])
    dur_cumsum = np.cumsum(dur)
    time = np.zeros(dur_cumsum[-1])
    zip_object = zip(act,dur)
    index = 0
    for a,d in zip_object:
        if a == 998:
           time[index:index+d] = 6
        elif a == 999:
            time[index:index+d] = 7
        else:
            time[index:index+d] = a
            index = index+d       
    plt.plot(time)
    plt.gca().set_yticks([0,1,2,3,4,5,6,7])
    plt.gca().set_yticklabels(['Unknown', 'Standing', 'Walking','In cubicle','At feed', 'At drinker','Out definite','Outside'])
    plt.show()
    
# function to plot distances (with histogram) for PA-data
def plot_distance_PA(df, tag_id1, tag_id2):
    cow_1 = df.loc[df['tag_id'] == tag_id1]
    cow_2 = df.loc[df['tag_id'] == tag_id2]
    x1,y1,z1 = positions(cow_1)
    x2,y2,z2 = positions(cow_2)
    
    times_1_start = list(cow_1['start'])
    times_1_end = list(cow_1['end'])
    times_2_start = list(cow_2['start'])
    times_2_end = list(cow_2['end'])
    
    act_1 = list(cow_1['activity_type'])
    act_2 = list(cow_2['activity_type'])
    
    distance_x = []
    distance_y = []
    
    distance_x.append(x1[0] - x2[0]) # initial distance
    distance_y.append(y1[0] - y2[0])
    i = 0 # index of times_1/x1/y1
    j = 0 # index of times_2/x2/y2
    act = np.ones(len(times_1_start) + len(times_2_start))
    times_comb = []
    times_comb.append(min(times_1_start[0], times_2_start[0]))
    while i < len(times_1_start)-1 or j < len(times_2_start)-1:
        if times_1_start[i] <= times_2_start[j]:           
            if i == len(times_1_start)-1:# if at end of times_1
                j = j+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2_start[j],times_1_start[i]))
            else:
                i = i+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2_start[j],times_1_start[i]))
        else:
            if j == len(times_2_start)-1: # if at end of times_2
                i = i+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2_start[j],times_1_start[i]))
            else:
                j = j+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2_start[j],times_1_start[i]))
        if act_1[i] == 3 or act_2[j] == 3:
            act[i+j] = 0

    distance = []
    temp = times_comb[0]
    times_comb = [x - temp for x in times_comb] # set initial time to zero
    times_comb_plot = [x*1/(3600*1000) for x in times_comb] 

    for i in range(len(distance_x)):
        distance.append(math.sqrt(distance_x[i]**2 + distance_y[i]**2))
    fig, ax =  plt.subplots(2,figsize=(6,6))
    ax[0].plot(times_comb_plot, distance)
    ax[0].set_title('Distance between cow ' + str(tag_id1) + ' and ' + str(tag_id2))
    ax[0].set_xlabel('Time [hours]')
    ax[0].set_ylabel('Distance [cm]')
    #plt.show()
    hist_arr = np.zeros(times_comb[-1])
    index = 0
    for i in range(len(times_comb)-1):
        if act[i] == 1:
            hist_arr[index:times_comb[i+1]] = distance[i]
        else:
            hist_arr[index:times_comb[i+1]] = 0
        index = times_comb[i+1]
    

    hist_arr = [i for i in hist_arr if i != 0]
    ax[1].hist(hist_arr, bins=50)
    ax[1].set_ylabel('#')
    ax[1].set_xlabel('Distance [cm]')
    plt.show()

# function to plot the distance between two cows when within a certain distance
# and when neither of the cows are sleeping
def plot_distance_thres_PA(df, tag_id1, tag_id2, threshold):
    cow_1 = df.loc[df['tag_id'] == tag_id1]
    cow_2 = df.loc[df['tag_id'] == tag_id2]
    x1,y1,z1, act1 = positions_PA(cow_1)
    x2,y2,z2, act2 = positions_PA(cow_2)
    
    times_1_start = list(cow_1['start'])
    times_1_end = list(cow_1['end'])
    times_2_start = list(cow_2['start'])
    times_2_end = list(cow_2['end'])
    
    distance_x = []
    distance_y = []
    
    distance_x.append(x1[0] - x2[0]) # initial distance
    distance_y.append(y1[0] - y2[0])
    i = 0 # index of times_1/x1/y1
    j = 0 # index of times_2/x2/y2
    act = np.ones(len(times_1_start) + len(times_2_start))
    times_comb = []
    times_comb.append(min(times_1_start[0], times_2_start[0]))
    while i < len(times_1_start)-1 or j < len(times_2_start)-1:
        if times_1_start[i] <= times_2_start[j]:           
            if i == len(times_1_start)-1:# if at end of times_1
                j = j+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2_start[j],times_1_start[i]))
            else:
                i = i+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2_start[j],times_1_start[i]))
        else:
            if j == len(times_2_start)-1: # if at end of times_2
                i = i+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2_start[j],times_1_start[i]))
            else:
                j = j+1
                distance_x.append(x1[i] - x2[j]) # new distance
                distance_y.append(y1[i] - y2[j])
                times_comb.append(min(times_2_start[j],times_1_start[i]))
        if act1[i] == 3 or act2[j] == 3:
            act[i+j] = 0

    distance = []
    temp = times_comb[0]
    times_comb = [x - temp for x in times_comb] # set initial time to zero
    times_copy = times_comb.copy()
    times_comb_plot = [x*1/(3600*1000) for x in times_comb] 

    for i in range(len(distance_x)):
        distance.append(math.sqrt(distance_x[i]**2 + distance_y[i]**2))
    
    distance_copy = distance.copy()
    
    for i in range(len(distance_copy)):
        if act[i] == 0:
            distance_copy[i] = np.nan
        elif distance_copy[i] > threshold:
            distance_copy[i] = np.nan

    for i in range(len(times_copy)):
        if np.isnan(distance_copy[i]):
            times_copy[i] = 0
    
        
    fig, ax =  plt.subplots(2,figsize=(6,6))
    ax[0].plot(times_comb_plot, distance_copy, 'go-')
    ax[0].set_title('Distance between cow ' + str(tag_id1) + ' and ' + str(tag_id2))
    ax[0].set_xlabel('Time [hours]')
    ax[0].set_ylabel('Distance [cm]')
    #plt.show()
    hist_arr = np.zeros(times_comb[-1])
    index = 0
    for i in range(len(times_comb)-1):
        if act[i] == 1:
            hist_arr[index:times_comb[i+1]] = distance_copy[i]
        else:
            hist_arr[index:times_comb[i+1]] = 0
        index = times_comb[i+1]
    

    hist_arr = [i for i in hist_arr if i != 0]
    ax[1].hist(hist_arr, bins=50)
    ax[1].set_xlabel('Distance [cm]')
    ax[1].set_ylabel('#')
    plt.show()

