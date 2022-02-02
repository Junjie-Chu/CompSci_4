import pandas as pd
import numpy as np
import math as m
import time 
from pycowview.data import csv_read_FA
from pycowview.manipulate import unique_cows
from pycowview.metrics import interaction_time
import networkx as nx
%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib as mpl
import itertools
import os
import community
from collections import defaultdict,Counter
import progressbar
import random
import itertools 
from sklearn.metrics.cluster import normalized_mutual_info_score

# custom function for NMI
def compute_NMI(p1,p2):
    list1 = []
    list2 = []
    key1set = set(sorted(p1))
    key2set = set(sorted(p2))
    keylist = list(key1set&key2set)
    keylist.sort()
    #print(len(key1set))
    #print(len(key2set))
    #print(len(keylist))
    i = 0
    for key in keylist:
        list1.append(p1.get(key,-1))
        list2.append(p2.get(key,-1))
        #i = i+1
        #print(i,key)
    #print(list1)
    #print(list2)
    return normalized_mutual_info_score(list1,list2)
 
# custom function for random simulation
def create_rand_adjacency(day):
    # create a random adjacency matrix of a specific day
    # compute the density
    graph = data_dict_list[day-1].get('Graph')
    density = nx.classes.function.density(graph)
    # create a basic matrix has the density
    AM = data_dict_list[day-1].get('AM_weighted')
    AM_rand = np.random.rand(AM.shape[0]*AM.shape[1]).reshape((AM.shape))
    AM_temp = np.zeros((AM_rand.shape))
    AM_temp[AM_rand <= density] = 1
    AM_temp[AM_rand > density] = 0

    # unweighted
    AM_up = np.triu(AM_temp)
    np.fill_diagonal(AM_up,0)
    AM_unweighted_rand = AM_up + AM_up.T

    # weighted
    AM_weighted_up = np.zeros((AM_up.shape))
    row,col = np.where(AM_up == 1)
    for i,j in zip(row,col):
        if AM_up[i][j] == 1:
            AM_weighted_up[i][j] = np.random.rand(1)
        else:
            pass
    AM_weighted_rand = AM_weighted_up + AM_weighted_up.T
    
    return AM_unweighted_rand, AM_weighted_rand 
  
# This part is for similarity of networks
# The method is to use what is called Eigenvector Similarity. 
# Basically, you calculate the Laplacian eigenvalues for the adjacency matrices of each of the graphs. 
# For each graph, find the smallest k such that the sum of the k largest eigenvalues constitutes at least 90% of the sum of all of the eigenvalues. 
# If the values of k are different between the two graphs, then use the smaller one. 
# The similarity metric is then the sum of the squared differences between the largest k eigenvalues between the graphs. 
# This will produce a similarity metric in the range [0, ∞), where values closer to zero are more similar.
def select_k(spectrum, minimum_energy = 0.9):
    running_total = 0.0
    total = sum(spectrum)
    if total == 0.0:
        return len(spectrum)
    for i in range(len(spectrum)):
        running_total += spectrum[i]
        if running_total / total >= minimum_energy:
            return i + 1
    return len(spectrum)
# This part is an example  
'''
for i in range(0,len(data_dict_list)-1):
    graph1 = data_dict_list[i].get('Graph')
    graph2 = data_dict_list[i+1].get('Graph')
    laplacian1 = nx.spectrum.laplacian_spectrum(graph1)
    laplacian2 = nx.spectrum.laplacian_spectrum(graph2)

    k1 = select_k(laplacian1)
    k2 = select_k(laplacian2)
    k = min(k1, k2)

    similarity = sum((laplacian1[:k] - laplacian2[:k])**2)
'''

# Get the N highest degree nodes of each day
def get_order_dict_N(_dict, N):
    result = Counter(_dict).most_common(N)
    topN = {}
    for k,v in result:
        topN[k] = v
    return topN
