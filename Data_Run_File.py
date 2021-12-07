import time
import numpy as np
import pandas as pd
from Data_Functions import detect_drop_inactive_tags, interaction_time_FA, interaction_time_FA_Area, define_Area
from pycowview.data import csv_read_FA
from pycowview.manipulate import unique_cows


def Interaction_time(files_to_run):
    # Parameters to change
    distance = 150
    time_step = 10

    for file in files_to_run:
        print(f'Starting calculations for: {file}')
        # Preprocess
        start_time = time.time()
        df = csv_read_FA(file, 0)
        df = detect_drop_inactive_tags(df)
        tag_list = unique_cows(df)
        print(len(tag_list))

        print('list fixed, proceding to interaction time calculations')
        t = interaction_time_FA(df, tag_list, distance, time_step)

        # Save results
        name_file = 'Time_'+file
        np.savetxt(name_file, t, delimiter=",")

        print(f'Done, this took {round(time.time()-start_time)}s to complete!')


def Interaction_time_steps_Area(files_to_run):
    # Parameters to change
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

        # Name the files
        name_bed_file = 'Time_Bed_'+file
        name_feed_file = 'Time_Feed_'+file
        name_robot_file = 'Time_Robot_'+file
        name_General_file = 'Time_General_'+file
        
        # save results
        np.savetxt(name_bed_file, t_bed, delimiter=",")
        np.savetxt(name_feed_file, t_feed, delimiter=",")
        np.savetxt(name_robot_file, t_robot, delimiter=",")
        np.savetxt(name_General_file, t_general, delimiter=",")

        print(f'Done, this took {round(time.time()-start_time)}s to complete!')


if __name__ == '__main__':
    #files_to_run = ['FA_20201016T000000UTC.csv', 'FA_20201017T000000UTC.csv', 'FA_20201018T000000UTC.csv', 'FA_20201019T000000UTC.csv', 'FA_20201020T000000UTC.csv', 'FA_20201021T000000UTC.csv', 'FA_20201022T000000UTC.csv', 'FA_20201023T000000UTC.csv', 'FA_20201024T000000UTC.csv', 'FA_20201025T000000UTC.csv', 'FA_20201026T000000UTC.csv', 'FA_20201027T000000UTC.csv', 'FA_20201028T000000UTC.csv', 'FA_20201029T000000UTC.csv']
    files_to_run = ['FA_20201016T000000UTC.csv']
    Interaction_time(files_to_run)
    Interaction_time_steps_Area(files_to_run)
