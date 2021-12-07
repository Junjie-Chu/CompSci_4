import numpy as np
import math as m
import pandas as pd
from pycowview.manipulate import unique_cows


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


class rectangle:
    def __init__(self, x1, x2, y1, y2, area):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.area = area

    def __contains__(self, x, y):
        if (self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2):
            return True
        else:
            return False

    def what_area(self):
        return self.area


# Function to read the data of the barn, only base 1
def csv_read_Barn(filename):
    df = pd.read_csv(filename, header=None, delimiter=';')
    df.columns = ['boundary', 'type', 'pointnum', 'x', 'y']
    return df

# File with area delimitation
def define_Area(filename, max_dist_from_area):
    df = csv_read_Barn(filename)
    rectangles = []
    area_names = ['bed', 'feed', 'robot']

    # What we want to save from the file
    bed_list = ['bed1', 'bed2', 'bed3', 'bed4',
                'bed5', 'bed6', 'bed7', 'bedinsemarea']
    feed_list = ['feedtable1', 'feedtable2', 'feedboxes']
    robot_list = ['robot']
    area_lists = [bed_list, feed_list, robot_list]

    for index, area_list in enumerate(area_lists):
        for area in area_list:
            to_ceck = df.loc[df['type'] == area]
            y = list(to_ceck['y'])
            x = list(to_ceck['x'])
            # if to_ceck.size == 20: # normal rectangle with 4 points
            temp_rectangle = rectangle(int(min(x))-max_dist_from_area, int(max(x))+max_dist_from_area, int(
                min(y))-max_dist_from_area, int(max(y))+max_dist_from_area, area_names[index])
            rectangles.append(temp_rectangle)
            # else: #not normal rectangel, might have to change for other files.
            #    pass
    return rectangles


def in_an_area(x, y, rectangles):
    for rectangle in rectangles:
        if rectangle.__contains__(x, y):
            return rectangle.what_area()
    return False

# function to detect and drop inactive tags for PA-data
def detect_drop_inactive_tags(df):
    ucows = unique_cows(df)
    to_drop = []
    for cow in ucows:
        temp = df.loc[df['tag_id'] == cow]
        y = list(temp['y'])
        if abs(max(y) - min(y)) <= 500 or max(y) > 10000:  # only check y-direction
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
    # array to save latest x position of each cow
    current_x = np.zeros(num_cows)
    # array to save latest y position of each cow
    current_y = np.zeros(num_cows)
    # matrix to see closeby cows at this time
    close_by = np.zeros((num_cows, num_cows))
    current_data = np.zeros(7)

    for k in range(num_data):
        current_data = data[k, :]
        current_data[3] = int(current_data[3] / 1000)  # Convert ms to s

        # Update x and y for all cows that move that time
        tag_index = tag_list.index(current_data[1])  # convert tag_id to index
        current_x[tag_index] = current_data[4]
        current_y[tag_index] = current_data[5]

        if current_data[3] >= next_timestep:
            # check distance for all cows
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

            # save our data
            next_timestep = current_data[3] + time_step
            int_time += time_step * close_by
    return int_time

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
    current_x = np.zeros(num_cows)
    current_y = np.zeros(num_cows)
    current_area = list(range(num_cows))
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

            # Calculate adjecancy Matrix
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

            # Convert to Area specific adjecancy Matricies
            result.initialize_time_matricies(close_by)
            for k in range(num_cows):
                if current_area[k]:
                    area = current_area[k]
                    getattr(result, area)(k)

            # Update our results
            result.update_time(time_step)
            next_timestep = current_data[3] + time_step

    return result.return_results()
