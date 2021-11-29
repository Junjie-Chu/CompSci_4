#import pandas as pd
import numpy as np
import math as m
#import time
from pycowview.data import csv_read_FA
from pycowview.manipulate import unique_cows
import progressbar


# function to detect and drop inactive tags for PA-data
def detect_drop_inactive_tags(df):
    ucows = unique_cows(df)
    to_drop = []
    for cow in ucows:
        temp = df.loc[df['tag_id'] == cow]
        y = list(temp['y'])
        x = list(temp['x'])
        if abs(max(y) - min(y)) <= 300:  # only check y-direction
            to_drop.append(cow)
        elif (min(y) > 10000):
            to_drop.append(cow)

    for i in range(len(to_drop)):
        df = df.drop(df[df.tag_id == to_drop[i]].index)  # drop tags

    return df


# Distance in cm and time_step in seconds
def interaction_time_FA(df, tag_id, distance, time_step):
    # sort data
    data = df.to_numpy()
    data = data[np.argsort(data[:, 3])]
    tag_list = tag_id.tolist()

    num_data = int(df.size / 7)
    num_cows = int(tag_id.size)
    next_timestep = int(data[0, 3] / 1000) + time_step  # First time step in s

    # track progress
    progress_count = int(num_data / 100)
    prog = 0

    # initialise matrices
    int_time = np.zeros((num_cows, num_cows))  # create the matrix with results
    current_x = np.zeros(num_cows)  # array to save latest x position of each cow
    current_y = np.zeros(num_cows)  # array to save latest y position of each cow 
    close_by = np.zeros((num_cows, num_cows))  # matrix to see closeby cows at this time
    current_data = np.zeros(7)

    for k in range(num_data):
        current_data = data[k, :]
        current_data[3] = int(current_data[3] / 1000)  # Convert ms to s

        # track progress
        if not (k) % progress_count:
            # print('Progress: ', k/progress_count, '%')
            bar.update(prog)
            prog += 1

        # Update x and y for all cows that move that time
        tag_index = tag_list.index(current_data[1])  # convert tag_id to index
        current_x[tag_index] = current_data[4]
        current_y[tag_index] = current_data[5]

        if current_data[3] >= next_timestep:
            # check distance for all cows
            for j in range(num_cows - 1):
                for i in range(j + 1, num_cows):
                    dis = m.hypot(current_x[j] - current_x[i], current_y[j] - current_y[i])
                    if dis <= distance and dis >= 1:
                        close_by[j, i] = 1
                        close_by[i, j] = 1
                    else:
                        close_by[j, i] = 0
                        close_by[i, j] = 0

            # save our data
            next_timestep = current_data[3] + time_step
            int_time += time_step * close_by
    return int_time


def main():
    bar = progressbar.ProgressBar(max_value=100)
    df0 = csv_read_FA('FA_example.csv', 0)
    df0 = detect_drop_inactive_tags(df0)
    cowlist = unique_cows(df0)

    distance = 150
    time_step = 10
    t = interaction_time_FA(df0, cowlist, distance, time_step)
    np.savetxt("Time_FA_example.csv", t, delimiter=",")


if __name__ == '__main__':
    main()
