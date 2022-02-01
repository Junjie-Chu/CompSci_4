###############################################################################
####                               METRICS                                 ####
###############################################################################

import math
import numpy as np
import pandas as pd

from .extras import positions, positions_PA
from .manipulate import unique_cows

# function to get matrix of average distances between cows
def get_distance(df, tag_id):
    res = np.zeros((len(tag_id),len(tag_id)))
    for k in range(len(tag_id)-1):
        for l in range(k+1, len(tag_id)):
            cow_1 = df.loc[df['tag_id'] == tag_id[k]]
            cow_2 = df.loc[df['tag_id'] == tag_id[l]]
            if cow_1.empty == False and cow_2.empty == False:
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
                            times_comb.append(times_2[j])
                        else:
                            i = i+1
                            distance_x.append(x1[i] - x2[j]) # new distance
                            distance_y.append(y1[i] - y2[j])
                            times_comb.append(times_1[i])
                    else:
                        if j == len(times_2)-1: # if at end of times_2
                            i = i+1
                            distance_x.append(x1[i] - x2[j]) # new distance
                            distance_y.append(y1[i] - y2[j])
                            times_comb.append(times_1[i])
                        else:
                            j = j+1
                            distance_x.append(x1[i] - x2[j]) # new distance
                            distance_y.append(y1[i] - y2[j])
                            times_comb.append(times_2[j])
            
                distance = []
                temp = times_comb[0]
                times_comb = [x - temp for x in times_comb] # set initial time to zero
                for i in range(len(distance_x)):
                    distance.append(math.sqrt(distance_x[i]**2 + distance_y[i]**2))

                res[k][l] = sum(distance)/len(distance)
    res_df = pd.DataFrame(data=res[0:,0:],index=tag_id, columns=tag_id)  # 1st row as the column names
    return res_df+res_df.T
   
# function same as get_distance() but for PA-data
# histogram not based on distances when either of the cows are sleeping/in cubicle
def get_distance_PA(df, tag_id):
    res_mean = np.zeros((len(tag_id),len(tag_id)))
    res_min = np.zeros((len(tag_id),len(tag_id)))
    for k in range(len(tag_id)-1):
        for l in range(k+1, len(tag_id)):
            cow_1 = df.loc[df['tag_id'] == tag_id[k]]
            cow_2 = df.loc[df['tag_id'] == tag_id[l]]
            if cow_1.empty == False and cow_2.empty == False:
                x1,y1,z1,act_1 = positions_PA(cow_1)
                x2,y2,z2,act_2 = positions_PA(cow_2)
                
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
                    if act_1[i] == 3 or act_2[j] == 3:
                        act[i+j] = 0
            
                distance = []
                temp = times_comb[0]
                times_comb = [x - temp for x in times_comb] # set initial time to zero
                for i in range(len(distance_x)):
                    if act[i] > 0:
                        distance.append(math.sqrt(distance_x[i]**2 + distance_y[i]**2))

                res_mean[k][l] = sum(distance)/len(distance) # average distance
                res_min[k][l] = min(distance) # minimum distance
    res_mean[np.tril_indices(res_mean.shape[0])] = np.nan
    res_min[np.tril_indices(res_min.shape[0])] = np.nan
    res_df_mean = pd.DataFrame(data=res_mean[0:,0:],index=tag_id, columns=tag_id)  # 1st row as the column names
    res_df_min = pd.DataFrame(data=res_min[0:,0:],index=tag_id, columns=tag_id)  
    return res_df_mean, res_df_min

# function to generate matrix of total time when cows are performing different activities 
def diff_act_PA(df, tag_id):
    res = np.zeros((len(tag_id),len(tag_id)))
    for k in range(len(tag_id)-1):
        for l in range(k+1, len(tag_id)):
            cow_1 = df.loc[df['tag_id'] == tag_id[k]]
            cow_2 = df.loc[df['tag_id'] == tag_id[l]]
            if cow_1.empty == False and cow_2.empty == False:
                x1,y1,z1,act_1 = positions_PA(cow_1)
                x2,y2,z2,act_2 = positions_PA(cow_2)
                
                times_1_start = list(cow_1['start'])
                times_1_end = list(cow_1['end'])
                times_2_start = list(cow_2['start'])
                times_2_end = list(cow_2['end'])
                
                i = 0 # index of times_1/x1/y1
                j = 0 # index of times_2/x2/y2
                act = 0
                time_idx = 0
                times_comb = []
                times_comb.append(min(times_1_start[0], times_2_start[0]))
                while i < len(times_1_start)-1 or j < len(times_2_start)-1:
                    if times_1_start[i] <= times_2_start[j]:           
                        if i == len(times_1_start)-1:# if at end of times_1
                            j = j+1
                            time_idx = time_idx + 1
                            times_comb.append(min(times_2_start[j],times_1_start[i]))
                        else:
                            i = i+1
                            time_idx = time_idx + 1
                            times_comb.append(min(times_2_start[j],times_1_start[i]))
                    else:
                        if j == len(times_2_start)-1: # if at end of times_2
                            i = i+1
                            time_idx = time_idx + 1
                            times_comb.append(min(times_2_start[j],times_1_start[i]))
                        else:
                            j = j+1
                            time_idx = time_idx + 1
                            times_comb.append(min(times_2_start[j],times_1_start[i]))
                    if act_1[i] != 3 and act_2[j] != 3: # if neither is in cubicle
                        if act_1[i] != act_2[j]:
                            act = act +  times_comb[time_idx] - times_comb[time_idx-1]
                        
                res[k][l] = act/(1000*60) # in minutes
    res[np.tril_indices(res.shape[0])] = np.nan
    res_df = pd.DataFrame(data=res[0:,0:],index=tag_id, columns=tag_id)  # 1st row as the column names
    return res_df

def time_at_feed(df):
    u_cows = unique_cows(df)
    feed_time = [0]*len(u_cows)
    for i in range(len(u_cows)):  # For each cow that has activity type "At feed"
        temp = df.loc[df['tag_id'] == u_cows[i]]
        temp = temp.loc[temp['activity_type'] == 4]

        for index, row in temp.iterrows():
            feed_time[i] += (row['end'] - row['start'])/1000
    return u_cows, feed_time

# function to generate matrix with time spent close to each other
def interaction_time(df, tag_id, dist):
    res = np.zeros((len(tag_id),len(tag_id)))
    for k in range(len(tag_id)-1):
        for l in range(k+1, len(tag_id)):
            cow_1 = df.loc[df['tag_id'] == tag_id[k]]
            cow_2 = df.loc[df['tag_id'] == tag_id[l]]
            if cow_1.empty == False and cow_2.empty == False:
                x1,y1,z1,act_1 = positions_PA(cow_1)
                x2,y2,z2,act_2 = positions_PA(cow_2)
                
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
                time_close = 0 # time spent close to each other
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
            
                temp = times_comb[0]
                times_comb = [x - temp for x in times_comb] # set initial time to zero
                for i in range(len(distance_x)-1):
                    if act[i] > 0:
                        temp_dist = math.sqrt(distance_x[i]**2 + distance_y[i]**2)
                        if temp_dist <= dist:
                            time_close = time_close + (times_comb[i+1]-times_comb[i]) # add time spent close                             

                res[k][l] = time_close/1000
                
    res[np.tril_indices(res.shape[0])] = np.nan
    res_df = pd.DataFrame(data=res[0:,0:],index=tag_id, columns=tag_id)  # 1st row as the column names
    return res_df

#Function to extract velocity vectors based on PA-data
def vector_analysis(df, tag_id, threshold):
    res_mat = np.zeros((len(tag_id),len(tag_id)))
    for k in range(len(tag_id)-1):
        for l in range(k+1, len(tag_id)):
            cow_1 = df.loc[df['tag_id'] == tag_id[k]]
            cow_2 = df.loc[df['tag_id'] == tag_id[l]]
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
            x_prod = np.ones(len(times_1_start) + len(times_2_start))
            
            while i < len(times_1_start)-2 or j < len(times_2_start)-2:
                if times_1_start[i] <= times_2_start[j]:           
                    if i == len(times_1_start)-2:# if at end of times_1
                        j = j+1
                        distance_x.append(x1[i] - x2[j]) # new distance
                        distance_y.append(y1[i] - y2[j])
                        times_comb.append(min(times_2_start[j],times_1_start[i]))
                        arr1 = np.array([x1[i + 1] - x1[i], y1[i + 1] - y1[i]])
                        arr2 = np.array([x2[j + 1] - x2[j], y2[j + 1] - y2[j]])
        
                        norm1 = np.linalg.norm(arr1)
                        norm2 = np.linalg.norm(arr2)
        
                        if norm1 != 0 and norm2 != 0:
                            arr1 = arr1 / np.linalg.norm(arr1)
                            arr2 = arr2 / np.linalg.norm(arr2)
        
                            temp_x = np.cross(arr1, arr2)
                            if temp_x>1:
                                temp_x = 1
                            x_prod[i + j] = np.arcsin(temp_x)
                        else:
                            x_prod[i + j] = np.nan
        
                    else:
                        i = i+1
                        distance_x.append(x1[i] - x2[j]) # new distance
                        distance_y.append(y1[i] - y2[j])
                        times_comb.append(min(times_2_start[j],times_1_start[i]))
                        arr1 = np.array([x1[i+1]-x1[i], y1[i+1] - y1[i]])
                        arr2 = np.array([x2[j+1]-x2[j], y2[j+1] - y2[j]])
        
                        norm1 = np.linalg.norm(arr1)
                        norm2 = np.linalg.norm(arr2)
        
                        if norm1 != 0 and norm2 != 0:
                            arr1 = arr1 / np.linalg.norm(arr1)
                            arr2 = arr2 / np.linalg.norm(arr2)
        
                            temp_x = np.cross(arr1, arr2)
                            if temp_x>1:
                                temp_x = 1
                            x_prod[i + j] = np.arcsin(temp_x)
                        else:
                            x_prod[i + j] = np.nan
        
                else:
                    if j == len(times_2_start)-2: # if at end of times_2
                        i = i+1
                        distance_x.append(x1[i] - x2[j]) # new distance
                        distance_y.append(y1[i] - y2[j])
                        times_comb.append(min(times_2_start[j],times_1_start[i]))
                        arr1 = np.array([x1[i + 1] - x1[i], y1[i + 1] - y1[i]])
                        arr2 = np.array([x2[j + 1] - x2[j], y2[j + 1] - y2[j]])
        
                        norm1 = np.linalg.norm(arr1)
                        norm2 = np.linalg.norm(arr2)
        
                        if norm1 != 0 and norm2 != 0:
                            arr1 = arr1 / np.linalg.norm(arr1)
                            arr2 = arr2 / np.linalg.norm(arr2)
        
                            temp_x = np.cross(arr1, arr2)
                            if temp_x>1:
                                temp_x = 1
                            x_prod[i + j] = np.arcsin(temp_x)
                        else:
                            x_prod[i + j] = np.nan
                    else:
                        j = j+1
                        distance_x.append(x1[i] - x2[j]) # new distance
                        distance_y.append(y1[i] - y2[j])
                        times_comb.append(min(times_2_start[j],times_1_start[i]))
                        arr1 = np.array([x1[i + 1] - x1[i], y1[i + 1] - y1[i]])
                        arr2 = np.array([x2[j + 1] - x2[j], y2[j + 1] - y2[j]])
        
                        norm1 = np.linalg.norm(arr1)
                        norm2 = np.linalg.norm(arr2)
        
                        if norm1 != 0 and norm2 != 0:
                            arr1 = arr1 / np.linalg.norm(arr1)
                            arr2 = arr2 / np.linalg.norm(arr2)
        
                            temp_x = np.cross(arr1, arr2)
                            if temp_x>1:
                                temp_x = 1
                            x_prod[i + j] = np.arcsin(temp_x)
                        else:
                            x_prod[i + j] = np.nan
                if act1[i] == 3 or act2[j] == 3:
                    act[i+j] = 0
        
            distance = []
            
            temp = times_comb[0]
            times_comb = [x - temp for x in times_comb] # set initial time to zero
            times_copy = times_comb.copy()
        
            for i in range(len(distance_x)):
                distance.append(math.sqrt(distance_x[i]**2 + distance_y[i]**2))
            
            distance_copy = distance.copy()
            
            for i in range(len(distance_copy)):
                if act[i] == 0:
                    x_prod[i] = np.nan
                elif distance_copy[i] > threshold or x_prod[i] > 15*180/math.pi:
                    x_prod[i] = np.nan
        
            res = []
            for i in range(len(times_copy)):
                if not np.isnan(x_prod[i]):
                    res.append(times_copy[i])
                    
            res_mat[k][l] = len(res)
                
    res_mat[np.tril_indices(res_mat.shape[0])] = np.nan
    res_df = pd.DataFrame(data=res_mat[0:,0:],index=tag_id, columns=tag_id)  # 1st row as the column names

    return res_df

#Function to extract velocity vectors based on PA-data
def vector_analysis_FA(df, tag_id, threshold, speed_thres): # vector analysis for FA-data (included speed)
    res_mat = np.zeros((len(tag_id),len(tag_id)))
    res_mat_time = np.zeros((len(tag_id),len(tag_id), 100000))
    for k in range(len(tag_id)-1):
        for l in range(k+1, len(tag_id)):
            cow_1 = df.loc[df['tag_id'] == tag_id[k]]
            cow_2 = df.loc[df['tag_id'] == tag_id[l]]
            x1,y1,z1 = positions(cow_1)
            x2,y2,z2 = positions(cow_2)
            
            times_1_start = list(cow_1['time'])
            times_2_start = list(cow_2['time'])
            
            temp_time1 = []
            temp_time2 = []
            
            distance_x = []
            distance_y = []
            speed1 = []
            speed2 = []
            
            distance_x.append(x1[0] - x2[0]) # initial distance
            distance_y.append(y1[0] - y2[0])
            arr1 = np.array([x1[1] - x1[0], y1[1] - y1[0]])
            arr2 = np.array([x2[1] - x2[0], y2[1] - y2[0]])
            speed1.append(math.sqrt(arr1[0]**2 + arr1[1]**2)/(times_1_start[1] - times_1_start[0]))
            speed2.append(math.sqrt(arr2[0]**2 + arr2[1]**2)/(times_2_start[1] - times_2_start[0]))
            i = 0 # index of times_1/x1/y1
            j = 0 # index of times_2/x2/y2

            times_comb = []
            times_comb.append(min(times_1_start[0], times_2_start[0]))
            x_prod = np.ones(len(times_1_start) + len(times_2_start))
            
            while i < len(times_1_start)-2 or j < len(times_2_start)-2:
                if times_1_start[i] <= times_2_start[j]:           
                    if i == len(times_1_start)-2:# if at end of times_1
                        j = j+1
                        distance_x.append(x1[i] - x2[j]) # new distance
                        distance_y.append(y1[i] - y2[j])
                        times_comb.append(min(times_2_start[j],times_1_start[i]))
                        arr1 = np.array([x1[i + 1] - x1[i], y1[i + 1] - y1[i]])
                        arr2 = np.array([x2[j + 1] - x2[j], y2[j + 1] - y2[j]])
                        speed1.append(math.sqrt(arr1[0]**2 + arr1[1]**2)/(times_1_start[i+1] - times_1_start[i]))
                        speed2.append(math.sqrt(arr2[0]**2 + arr2[1]**2)/(times_2_start[j+1] - times_2_start[j]))
                        temp_time1.append(times_1_start[i])
                        temp_time2.append(times_2_start[j])
        
                        norm1 = np.linalg.norm(arr1)
                        norm2 = np.linalg.norm(arr2)
        
                        if norm1 != 0 and norm2 != 0:
                            arr1 = arr1 / np.linalg.norm(arr1)
                            arr2 = arr2 / np.linalg.norm(arr2)
        
                            temp_x = np.cross(arr1, arr2)
                            if temp_x>1:
                                temp_x = 1
                            x_prod[i + j] = np.arcsin(temp_x)
                        else:
                            x_prod[i + j] = np.nan
        
                    else:
                        i = i+1
                        distance_x.append(x1[i] - x2[j]) # new distance
                        distance_y.append(y1[i] - y2[j])
                        times_comb.append(min(times_2_start[j],times_1_start[i]))
                        arr1 = np.array([x1[i+1]-x1[i], y1[i+1] - y1[i]])
                        arr2 = np.array([x2[j+1]-x2[j], y2[j+1] - y2[j]])
                        
                        speed1.append(math.sqrt(arr1[0]**2 + arr1[1]**2)/(times_1_start[i+1] - times_1_start[i]))
                        speed2.append(math.sqrt(arr2[0]**2 + arr2[1]**2)/(times_2_start[j+1] - times_2_start[j]))
                        temp_time1.append(times_1_start[i])
                        temp_time2.append(times_2_start[j])
        
                        norm1 = np.linalg.norm(arr1)
                        norm2 = np.linalg.norm(arr2)
        
                        if norm1 != 0 and norm2 != 0:
                            arr1 = arr1 / np.linalg.norm(arr1)
                            arr2 = arr2 / np.linalg.norm(arr2)
        
                            temp_x = np.cross(arr1, arr2)
                            if temp_x>1:
                                temp_x = 1
                            x_prod[i + j] = np.arcsin(temp_x)
                        else:
                            x_prod[i + j] = np.nan
        
                else:
                    if j == len(times_2_start)-2: # if at end of times_2
                        i = i+1
                        distance_x.append(x1[i] - x2[j]) # new distance
                        distance_y.append(y1[i] - y2[j])
                        times_comb.append(min(times_2_start[j],times_1_start[i]))
                        arr1 = np.array([x1[i + 1] - x1[i], y1[i + 1] - y1[i]])
                        arr2 = np.array([x2[j + 1] - x2[j], y2[j + 1] - y2[j]])
                        
                        speed1.append(math.sqrt(arr1[0]**2 + arr1[1]**2)/(times_1_start[i+1] - times_1_start[i]))
                        speed2.append(math.sqrt(arr2[0]**2 + arr2[1]**2)/(times_2_start[j+1] - times_2_start[j]))
                        temp_time1.append(times_1_start[i])
                        temp_time2.append(times_2_start[j])
        
                        norm1 = np.linalg.norm(arr1)
                        norm2 = np.linalg.norm(arr2)
        
                        if norm1 != 0 and norm2 != 0:
                            arr1 = arr1 / np.linalg.norm(arr1)
                            arr2 = arr2 / np.linalg.norm(arr2)
        
                            temp_x = np.cross(arr1, arr2)
                            if temp_x>1:
                                temp_x = 1
                            x_prod[i + j] = np.arcsin(temp_x)
                        else:
                            x_prod[i + j] = np.nan
                    else:
                        j = j+1
                        distance_x.append(x1[i] - x2[j]) # new distance
                        distance_y.append(y1[i] - y2[j])
                        times_comb.append(min(times_2_start[j],times_1_start[i]))
                        arr1 = np.array([x1[i + 1] - x1[i], y1[i + 1] - y1[i]])
                        arr2 = np.array([x2[j + 1] - x2[j], y2[j + 1] - y2[j]])
                        
                        speed1.append(math.sqrt(arr1[0]**2 + arr1[1]**2)/(times_1_start[i+1] - times_1_start[i]))
                        speed2.append(math.sqrt(arr2[0]**2 + arr2[1]**2)/(times_2_start[j+1] - times_2_start[j]))
                        temp_time1.append(times_1_start[i])
                        temp_time2.append(times_2_start[j])
        
                        norm1 = np.linalg.norm(arr1)
                        norm2 = np.linalg.norm(arr2)
        
                        if norm1 != 0 and norm2 != 0:
                            arr1 = arr1 / np.linalg.norm(arr1)
                            arr2 = arr2 / np.linalg.norm(arr2)
        
                            temp_x = np.cross(arr1, arr2)
                            if temp_x>1:
                                temp_x = 1
                            x_prod[i + j] = np.arcsin(temp_x)
                        else:
                            x_prod[i + j] = np.nan
        
            distance = []
            res_time = []
            check_time = 0
            
            temp = times_comb[0]
            times_comb = [x - temp for x in times_comb] # set initial time to zero
            times_copy = times_comb.copy()
        
            for i in range(len(distance_x)):
                distance.append(math.sqrt(distance_x[i]**2 + distance_y[i]**2))
            
            distance_copy = distance.copy()
            
            for i in range(len(distance_copy)):
                if distance_copy[i] > threshold or x_prod[i] > 15*180/math.pi: # within 14 degrees
                    x_prod[i] = np.nan
                elif speed1[i] > speed_thres:
                    x_prod[i] = np.nan
                elif speed2[i] > speed_thres:
                    x_prod[i] = np.nan
                else:
                   res_time.append(min(temp_time1[i], temp_time2[i]))
                   check_time += 1
        
            res = []
            for i in range(len(times_copy)):
                if not np.isnan(x_prod[i]):
                    res.append(times_copy[i])
            if check_time > 0:
                if check_time > 1:
                    for i in range(len(res_time)):
                        res_mat_time[k][l][i] = res_time[i]
                else:
                    res_mat_time[i] = res_time
            res_mat[k][l] = len(res)
                
    res_mat[np.tril_indices(res_mat.shape[0])] = np.nan
    res_df = pd.DataFrame(data=res_mat[0:,0:],index=tag_id, columns=tag_id)  # 1st row as the column names
    
    temp_shape = res_mat_time.shape
    new = res_mat_time.reshape(-1,temp_shape[2], order = "C")

    time_thresh = 10*1000
    temp_shape = new.shape
    result = np.zeros(temp_shape)
    result_count = np.zeros(temp_shape)

    for i in range(len(new[:, 0])):
        temp = new[i, :]
        temp = temp[temp != 0]
        if temp.shape != (0,):
            result_vector = []
            counter = 1
            count_vector =[]
            for j in range(len(temp)-1, 1, -1):
                if not temp[j]-temp[j-1] < time_thresh:
                    count_vector.append(counter)
                    counter = 1
                    result_vector.append(temp[j])
                else:
                    counter +=1
            result_vector.append(temp[0])
            count_vector.append(counter)            
            result[i, 0:len(result_vector)] = result_vector
            result_count[i, 0:len(count_vector)] = count_vector
        else:
            print("EMPTY")

    new = result

    col1 = []
    col2 = []
    for i in range(len(tag_id)):
        temp = [tag_id[i]]
        temp = temp*(len(tag_id))
        col1.extend(temp)
        for j in range(len(tag_id)):
            col2.append(tag_id[j])
  
    col1 = np.transpose(np.asarray(col1))
    col2 = np.transpose(np.asarray(col2))
    result_count = np.insert(result_count, 0, col2, axis=1)
    result_count = np.insert(result_count, 0, col1, axis=1)
    new = np.insert(new, 0, col2, axis=1)
    new = np.insert(new, 0, col1, axis=1)
                
    return res_df, new, result_count


# function to get intersection between two dataframes
def intersect(df1, df2):
    
    df1_tags1 = list(df1.index.get_level_values(level=0))
    df1_tags2 = list(df1.index.get_level_values(level=1))
    list_1 = np.array((df1_tags1,df1_tags2)).transpose()
    
    df2_tags1 = list(df2.index.get_level_values(level=0))
    df2_tags2 = list(df2.index.get_level_values(level=1))
    list_2 = np.array((df2_tags1,df2_tags2)).transpose()
        
    res = np.zeros(shape=(len(df1_tags1),2))

    idx = 0
    for i in range(len(df1_tags1)):
        if any((list_1[:]==list_2[i]).all(1)):
            res[idx] = list_2[i]
            idx = idx + 1
    
    res = res[~np.all(res == 0, axis=1)]
    return res

#Function to produce displacement textfiles
def displacement(df_PA, u_cows, tag_id, textfile = 'result.txt'):
    cow = df_PA.loc[df_PA['tag_id'] == tag_id]
    x, y, z, act = positions_PA(cow)

    indices = [i for i, x in enumerate(act) if x == 4]

    cow = cow.iloc[indices]

    start = list(cow['start'])
    end = list(cow['end'])
    x, y, z, act= positions_PA(cow)

    res_time = []
    res_pos = []
    for i in range(len(indices)-1):
        if  5*1000 < start[i+1] - end[i] < 30*1000 and y[i]>3000 and 100<abs(y[i]-y[i+1]): #and end[i]-start[i]>10*1000:
            res_time.append(end[i])
            res_pos.append((x[i], y[i]))

    #print(tag_id)
    #print(res_time)
    with open(textfile, "a") as file:
        file.write("Original cow: " + str(tag_id) + "\n")
        print("Original cow: " + str(tag_id))
    
        for i in range(len(res_time)):
    
            hostile_cows = []
            for cow in u_cows:
                if cow != tag_id:
                    cow_subset = df_PA.loc[df_PA['tag_id'] == cow]
                    for index, row in cow_subset.iterrows():
                        if 0 < res_time[i]-row['start']<5*1000 and 100 >(math.sqrt(math.pow(row['x']-res_pos[i][0], 2) + math.pow(row['y']-res_pos[i][1], 2))):
                            hostile_cows.append(cow)
            if len(hostile_cows)!= 0:
                file.write(str(res_time[i]))
                file.write((str(hostile_cows)))
                file.write("\n")
                print(res_time[i])
                print(hostile_cows)
    #file.close()