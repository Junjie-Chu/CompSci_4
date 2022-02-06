import pandas as pd
import numpy as np
import math as m
import time
from pycowview.data import csv_read_FA
from pycowview.manipulate import unique_cows
from pycowview.metrics import interaction_time
import networkx as nx
import matplotlib.pyplot as plt

def Create_Adj_Matrix_from_FA(FA,tmin):
    """
        Create_Adj_Matrix creates the binary adjacency matrix using numpy.
        Creates a binary adjacency matrix from the FA data

        :param FA: The FA data in numpy
        :param tmin: the minimum time, in seconds, needed to become connected
        :return: Adjacecny matrix in numpy
        """
    nrcows=int( m.sqrt(FA.size))
    print(str(nrcows)+ " This is how many cows ther are")
    adj_mat = np.zeros((nrcows,nrcows)) #create the matrix with results
    for k in range(nrcows-2):
        for j in range(nrcows-k-1):
            if (FA[k,j+1]>=tmin):
                adj_mat[k,k+j+1]=1
                adj_mat[k+j+1,k]=1
    return adj_mat

def Create_weighted_Adj_Matrix(OM,min_time):
    """
        Create_weighted_Adj_Matrix creates a weighted adjacency matrix using numpy.
        A adjacency matrix where the connections are between zero and one depending on the time spent with that cow.

        :param OM: The time matrix in numpy
        :param min_time: The minimum time, in seconds, needed to spend together to become a connection
        :return: weighted adjacency matrix in numpy
        """
    # load original matrix from csv and process it to be an adjacency Matrix
    #OM = np.loadtxt(filename,delimiter=",")
    AM = np.zeros((OM.shape))
    # just consider if there is an edge between two cows, the edge is unweighted
    maxnr=np.amax(OM)
    AM=np.where(OM<epsilon,0*OM,(OM-min_time)/(maxnr-min_time))
    np.fill_diagonal(AM,0)
    return AM



def Degree_Matrix(OM):
    """
    Degree_Matrix creates the degree matrix using numpy.
    a matrix where the diagonals are the amount of edges that node is connected to.

    :param OM: The Adjacency matrix in numpy
    :return: Degree matrix in numpy
    """
    AM = np.zeros((OM.shape))
    rows, columns = AM.shape
    rowlist = range(rows)
    for k in rowlist:
        degnr = sum(OM[k])
        AM[k][k] = degnr
        print(AM[k][k])
    return AM


def Laplacian_Matrix(DM, AM):
    """
    Laplacian_Matrix creates the laplacian matrix using numpy.
    LM=DM-AM
    :param DM: The Degree matrix in numpy
    :param AM: The Adjacency matrix in numpy
    :return: Laplacian matrix in numpy
    """
    LM = np.zeros((AM.shape))
    LM = DM - AM
    return LM