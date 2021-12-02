from typing import Sized
import pandas as pd


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
    return None


rectangles = define_Area('barn_WimBos.csv', 0)
print(in_an_area(1100, 3000, rectangles))
