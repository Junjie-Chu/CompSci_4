import pandas as pd
import numpy as np
from numpy import linalg as LA
from scipy import linalg as LB
import math as m
import time
from pycowview.data import csv_read_FA
from pycowview.manipulate import unique_cows
from pycowview.metrics import interaction_time
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import itertools
import os
from collections import defaultdict
import random


def Algebraic_Connectivity(AM):

    lam = LA.eig(AM)
    alg_con=lam[1]
    return lam

def Eigenvector_centrality(AM):
    G= nx.from_numpy_matrix(AM,parallel_edges=False)
    A=nx.eigenvector_centrality(G)
    return A

def hist_Eigenvec_cent(eigenvecs):
    plt.hist(eigenvecs)