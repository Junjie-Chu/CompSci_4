import time
import numpy as np
from Interaction_time_steps import detect_drop_inactive_tags, interaction_time_FA
from Interaction_time_steps_areas import interaction_time_FA_Area
from pycowview.data import csv_read_FA
from pycowview.manipulate import unique_cows
from pycowview.plot import plot_barnV2
from Barn import define_Area, rectangle


def Interaction_time_steps():
    # Parameters to change
    files_to_run = ['FA_20201016T000000UTC.csv', 'FA_20201017T000000UTC.csv']
    distance = 150
    time_step = 10

    for file in files_to_run:
        print(f'Starting calculations for: {file}')
        # Preprocess
        start_time = time.time()
        df = csv_read_FA(file, 0)
        df = detect_drop_inactive_tags(df)
        tag_list = unique_cows(df)

        print('list fixed, proceding to interaction time calculations')
        t = interaction_time_FA(df, tag_list, distance, time_step)

        # Save results
        name_file = 'Time_'+file
        np.savetxt(name_file, t, delimiter=",")

        print(f'Done, this took {round(time.time()-start_time)}s to complete!')


def Interaction_time_steps_Area():
    # Parameters to change
    files_to_run = ['FA_example.csv']
    barnfile = 'barn_WimBos.csv'
    additional_dist_for_area_selection = 0
    distance = 150
    time_step = 10

    for file in files_to_run:
        print(f'Starting calculations for: {file}')
        # Preprocess
        start_time = time.time()
        df = csv_read_FA(file, 0)
        df = detect_drop_inactive_tags(df)
        tag_list = unique_cows(df)

        print('list fixed, proceding to interaction time calculations')
        # Interaction time
        rectangles = define_Area(barnfile, additional_dist_for_area_selection)
        t_bed, t_feed, t_robot, t_general = interaction_time_FA_Area(
            df, tag_list, distance, time_step, rectangles)

        # Save to files
        name_bed_file = 'Time_Bed_'+file
        np.savetxt(name_bed_file, t_bed, delimiter=",")
        name_feed_file = 'Time_Feed_'+file
        np.savetxt(name_feed_file, t_feed, delimiter=",")
        name_robot_file = 'Time_Robot_'+file
        np.savetxt(name_robot_file, t_robot, delimiter=",")
        name_General_file = 'Time_General_'+file
        np.savetxt(name_General_file, t_general, delimiter=",")

        print(f'Done, this took {round(time.time()-start_time)}s to complete!')


if __name__ == '__main__':
    Interaction_time_steps()
    #Interaction_time_steps_Area():
