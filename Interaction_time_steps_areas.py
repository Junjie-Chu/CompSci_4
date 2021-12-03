#import pandas as pd
import numpy as np
import math as m
#import time
from pycowview.data import csv_read_FA
from pycowview.manipulate import unique_cows
from Barn import in_an_area


class results:
    def __init__(self, num_cows):
        self.res_bed = np.zeros((num_cows, num_cows))
        self.res_feed = np.zeros((num_cows, num_cows))
        self.res_robot = np.zeros((num_cows, num_cows))
        self.res_general = np.zeros((num_cows, num_cows))
        self.current_area = list(range(num_cows))
        self.num_cows = num_cows

    def update_area(self, current_x, current_y, rectangles):
        for k in range(self.num_cows):
            self.current_area[k] = in_an_area(
                current_x[k], current_y[k], rectangles)
        return self.current_area

    def initialize_time_matricies(self, close_by):
        self.int_time_bed = np.zeros((self.num_cows, self.num_cows))
        self.int_time_feed = np.zeros((self.num_cows, self.num_cows))
        self.int_time_robot = np.zeros((self.num_cows, self.num_cows))
        self.int_time_general = close_by

    def bed(self, index):
        for i in range(self.num_cows):
            if self.int_time_general[i, index] == 1:
                self.int_time_bed[i, index], self.int_time_bed[index, i] = 1, 1
                self.int_time_general[i,
                                      index], self.int_time_general[index, i] = 0, 0

    def feed(self, index):
        for i in range(self.num_cows):
            if self.int_time_general[i, index] == 1:
                self.int_time_feed[i,
                                   index], self.int_time_feed[index, i] = 1, 1
                self.int_time_general[i,
                                      index], self.int_time_general[index, i] = 0, 0

    def robot(self, index):
        for i in range(self.num_cows):
            if self.int_time_general[i, index] == 1:
                self.int_time_robot[i,
                                    index], self.int_time_robot[index, i] = 1, 1
                self.int_time_general[i,
                                      index], self.int_time_general[index, i] = 0, 0

    def update_time(self, time):
        self.res_bed += time*self.int_time_bed
        self.res_feed += time*self.int_time_feed
        self.res_robot += time*self.int_time_robot
        self.res_general += time*self.int_time_general

    def return_results(self):
        return self.res_bed, self.res_feed, self.res_robot, self.res_general

# function to detect and drop inactive tags for PA-data


def detect_drop_inactive_tags(df):
    ucows = unique_cows(df)
    to_drop = []
    for cow in ucows:
        temp = df.loc[df['tag_id'] == cow]
        y = list(temp['y'])
        #x = list(temp['x'])
        if abs(max(y) - min(y)) <= 300:  # only check y-direction
            to_drop.append(cow)
        elif (min(y) > 10000):
            to_drop.append(cow)

    for i in range(len(to_drop)):
        df = df.drop(df[df.tag_id == to_drop[i]].index)  # drop tags

    return df

# Function to calculate interaction time, sorted into areas
# Distance in cm and time_step in seconds


def interaction_time_FA_Area(df, tag_id, distance, time_step, rectangles):
    # sort data
    data = df.to_numpy()
    data = data[np.argsort(data[:, 3])]
    tag_list = tag_id.tolist()

    num_data = int(df.size / 7)
    num_cows = int(tag_id.size)
    next_timestep = int(data[0, 3] / 1000) + time_step  # First time step in s

    # initialise matrices
    # array to save latest x position of each cow
    current_x = np.zeros(num_cows)
    # array to save latest y position of each cow
    current_y = np.zeros(num_cows)
    current_area = list(range(num_cows))
    # matrix to see closeby cows at this time
    close_by = np.zeros((num_cows, num_cows))
    current_data = np.zeros(7)

    result = results(num_cows)

    for k in range(num_data):
        current_data = data[k, :]
        current_data[3] = int(current_data[3] / 1000)  # Convert ms to s

        # Update x and y
        tag_index = tag_list.index(current_data[1])  # convert tag_id to index
        current_x[tag_index] = current_data[4]
        current_y[tag_index] = current_data[5]

        if current_data[3] >= next_timestep:
            # check area for all cows
            current_area = result.update_area(current_x, current_y, rectangles)

            for j in range(num_cows - 1):
                for i in range(j + 1, num_cows):
                    dis = m.hypot(
                        current_x[j] - current_x[i], current_y[j] - current_y[i])
                    if dis <= distance and dis >= 1:
                        close_by[j, i] = 1
                        close_by[i, j] = 1
                    else:
                        close_by[j, i] = 0
                        close_by[i, j] = 0

            result.initialize_time_matricies(close_by)

            for k in range(num_cows):
                if current_area[k]:
                    area = current_area[k]
                    getattr(result, area)(k)

            result.update_time(time_step)
            next_timestep = current_data[3] + time_step

    return result.return_results()
