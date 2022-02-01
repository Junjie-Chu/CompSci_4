###############################################################################
####                              ANIMATION                                ####
###############################################################################

import matplotlib.pyplot as plt
import pandas as pd
from random import randint
import math
import matplotlib.lines as mlines
import matplotlib.patches as pat
from matplotlib.animation import FuncAnimation
from matplotlib import transforms
from datetime import datetime

from plot import plot_barnV2, plot_all_cows
from extras import positions
from plot import plot_barn

pause = False

def animate_cowsV2(df, cowID_1, cowID_2, barn_filename, interesting_time, save_path='n'):

    f, ax1 = plot_barnV2(barn_filename) #Get barn koordinates

    ax1, nearby_cows = plot_all_cows(ax1, df, interesting_time, [cowID_1, cowID_2]) #Get all records of gray cows

    unimportant_cows = nearby_cows.copy()

    nearby_cows.append(cowID_1) #Ad interesting cows
    nearby_cows.append(cowID_2)


    df_cows = df[df['tag_id'].isin(nearby_cows)]

    df_cows = df_cows.sort_values('time')

    x, y, z = positions(df_cows)

    tag_id = list(df_cows['tag_id'])

    time = list(df_cows['time'])

    timestrings = []

    #This counts how many times the ineresting cows move and base the number of frames presented on this
    frames = 0
    for tag in tag_id:
        if tag == cowID_1 or tag == cowID_2:
            frames +=1

    #This makes the timestrings that is printed and adjust them for timezone and daylight savings
    for timestamp in time:
        timestrings.append(datetime.fromtimestamp((timestamp/1000)-7200))

    ax1.change_geometry(2, 1, 1)
    ax2 = f.add_subplot(212)
    ax1.set_aspect('equal', 'datalim')


    plt.tight_layout()

    pos1 = ax1.get_position().bounds
    pos2 = ax2.get_position().bounds

    new_pos1 = [pos1[0], 0.25, pos1[2], 0.7]
    new_pos2 = [pos2[0], pos2[1], pos2[2], 0.1]
    ax1.set_position(new_pos1)
    ax2.set_position(new_pos2)
    
    
    xdata1, ydata1 = [x[tag_id.index(cowID_1)]], [y[tag_id.index(cowID_1)]]

    xdata2, ydata2 = [x[tag_id.index(cowID_2)]], [y[tag_id.index(cowID_2)]]

    dist, time = [], []

    list_of_dots =[]

    for i in range(len(unimportant_cows)+2):
        if i == len(unimportant_cows):
            list_of_dots.append(ax1.plot([], [], '-', alpha = 0.8)[0])
            list_of_dots.append(ax1.plot([], [], 'co', label='Cow ' + str(cowID_1), alpha = 0.5)[0])
            
        elif i == len(unimportant_cows)+1:
            list_of_dots.append(ax1.plot([], [], '-', alpha = 0.8)[0])
            list_of_dots.append(ax1.plot([], [], 'yo', label='Cow ' + str(cowID_2), alpha = 0.5)[0])
            
        else:
            list_of_dots.append(ax1.plot([], [], 'o', color='tab:gray', alpha = 0.8)[0])

    list_of_dots.append(ax2.plot([], [], 'r-')[0])

    ax1.legend(loc='upper right')

    ax1.set_ylim(0, 3340)
    ax1.set_xlim(0, 8738)
    ax2.set_xlim(timestrings[0], timestrings[len(timestrings) - 1])

    ax2.set_ylim(0, 10000)
    date1 = timestrings[0]
    date2 = timestrings[len(timestrings) - 1]
    ax1.set_title("Plot of two cows between " + date1.strftime("%d %b %Y %H:%M") + " - " +
                  date2.strftime("%d %b %Y %H:%M"), fontsize=8)
    ax2.set_ylabel('Distance(cm)')
    ax2.set_xlabel('Time of day')

    def run_animation(): #If the window is clicked, the animation pauses
        ani_running = True
        i = 0
        def onClick(event):
            nonlocal ani_running
            if ani_running:
                ani.event_source.stop()
                ani_running = False
            else:
                ani.event_source.start()
                ani_running = True


        def update(frame): #Update function for the animation, what happens each frame
            nonlocal i
            if not pause:
                check = 0
                while check == 0:
                    if tag_id[i] == cowID_1:
                        check = 1
                        xdata1.append(x[i])  # new distance
                        ydata1.append(y[i])
                        xdata2.append(xdata2[-1])  # new distance
                        ydata2.append(ydata2[-1])

                    elif tag_id[i] == cowID_2:
                        check = 1
                        xdata2.append(x[i])  # new distance
                        ydata2.append(y[i])
                        xdata1.append(xdata1[-1])  # new distance
                        ydata1.append(ydata1[-1])

                    else:
                        index = unimportant_cows.index(tag_id[i])
                        list_of_dots[index].set_data(y[i], x[i])

                    i += 1

                list_of_dots[-5].set_data(ydata1, xdata1)
                list_of_dots[-4].set_data(ydata1[-1], xdata1[-1])
                list_of_dots[-3].set_data(ydata2, xdata2)
                list_of_dots[-2].set_data(ydata2[-1], xdata2[-1])

                dist.append(math.sqrt(math.pow(xdata1[-1]-xdata2[-1], 2) + math.pow(ydata1[-1]-ydata2[-1], 2)))

                time.append((timestrings[i]))

                list_of_dots[-1].set_data(time, dist)

            return list_of_dots

        f.canvas.mpl_connect('button_press_event', onClick)
        ani = FuncAnimation(f, update, frames=frames, blit=True, interval=50, repeat=False)

        #HAndles saving the animation if filename is given
        if save_path != 'n':
            try:
                ani.save(save_path)
            except:
                print('Wrong filepath')

        plt.show()

    run_animation()








def animate_cows(df, cowID_1, cowID_2, barn_filename, save_path='n'):

    cow_1 = df.loc[df['tag_id'] == cowID_1]

    cow_2 = df.loc[df['tag_id'] == cowID_2]

    x1, y1, z1 = positions(cow_1)
    x2, y2, z2 = positions(cow_2)

    time1 = list(cow_1['time'])
    time2 = list(cow_2['time'])

    timestrings1= []
    timestrings2 = []

    for timestamp1 in time1:
        timestrings1.append(datetime.fromtimestamp((timestamp1/1000)-7200))

    for timestamp2 in time2:
        timestrings2.append(datetime.fromtimestamp((timestamp2 / 1000) - 7200))

    f, ax1 = plot_barn(barn_filename)


    ax1.change_geometry(2, 1, 1)
    ax2 = f.add_subplot(212)

    plt.tight_layout()

    pos1 = ax1.get_position().bounds
    pos2 = ax2.get_position().bounds

    new_pos1 = [pos1[0], 0.25, pos1[2], 0.7]
    new_pos2 = [pos2[0], pos2[1], pos2[2], 0.1]

    ax1.set_position(new_pos1)
    ax2.set_position(new_pos2)

    xdata1, ydata1 = [], []
    ln1, = ax1.plot([], [], '-')
    xdata2, ydata2 = [], []
    ln2, = ax1.plot([], [], '-')

    d1, = ax1.plot([], [], 'co', label='Cow '+ str(cowID_1))
    d2, = ax1.plot([], [], 'yo', label='Cow '+ str(cowID_2))

    ax1.legend(loc='upper left')

    dist, time = [], []
    dist_plot, = ax2.plot([], [], 'r-')

    def run_animation():
        ani_running = True
        i = 0
        j = 0
        def onClick(event): #If the window is clicked, the gif pauses
            nonlocal ani_running
            if ani_running:
                ani.event_source.stop()
                ani_running = False
            else:
                ani.event_source.start()
                ani_running = True

        def init():
            ax1.set_xlim(0, 3340)
            ax1.set_ylim(0, 8738)
            ax2.set_xlim(timestrings1[0], timestrings1[len(timestrings1)-1])

            ax2.set_ylim(0, 10000)
            date1 = timestrings1[0]
            date2 = timestrings1[len(timestrings1)-1]
            ax1.set_title("Plot of two cows between " + date1.strftime("%d %b %Y %H:%M") + " - " +
                          date2.strftime("%d %b %Y %H:%M"), fontsize=8)
            ax2.set_ylabel('Distance(cm)')
            ax2.set_xlabel('Time of day')

            return ln1, ln2, d1, d2, dist_plot

        def update(frame):
            nonlocal i
            nonlocal j
            if not pause:
                if time1[i] <= time2[j]:
                    if i == len(time1) - 1:  # if at end of times_1
                        j = j + 1
                        xdata2.append(x2[j])  # new distance
                        ydata2.append(y2[j])
                        xdata1.append(x1[i])  # new distance
                        ydata1.append(y1[i])
                    else:
                        i = i + 1
                        xdata1.append(x1[i])  # new distance
                        ydata1.append(y1[i])
                        xdata2.append(x2[j])  # new distance
                        ydata2.append(y2[j])
                else:
                    if j == len(time2) - 1:  # if at end of times_2
                        i = i + 1
                        xdata1.append(x1[i])  # new distance
                        ydata1.append(y1[i])
                        xdata2.append(x2[j])  # new distance
                        ydata2.append(y2[j])
                    else:
                        j = j + 1
                        xdata2.append(x2[j])  # new distance
                        ydata2.append(y2[j])
                        xdata1.append(x1[i])  # new distance
                        ydata1.append(y1[i])

                ln1.set_data(xdata1, ydata1) #Uppdate the plot with the data
                d1.set_data(x1[i], y1[i])
                ln2.set_data(xdata2, ydata2)
                d2.set_data(x2[j], y2[j])
                dist.append(math.sqrt(math.pow(x1[i]-x2[j], 2) + math.pow(y1[i]-y2[j], 2)))

                if time1[i]<time2[j]: #Uppdate the correct time
                    time.append((timestrings1[i]))
                else:
                    time.append((timestrings2[j]))


                dist_plot.set_data(time, dist)

            return ln1, ln2, d1, d2, dist_plot

        f.canvas.mpl_connect('button_press_event', onClick)
        ani = FuncAnimation(f, update, frames=len(time1)+len(time2)-2, init_func=init, blit=True, interval=1, repeat=False) #Main animationfunction
        if save_path != 'n': #If a filename is given, the gif is saved
            try:
                ani.save(save_path)
            except:
                print('Wrong filepath')

        plt.show()

    run_animation()    
 