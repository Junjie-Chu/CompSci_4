import pandas as pd
import numpy as np
import math as m
import time 
from pycowview.data import csv_read_FA
from pycowview.manipulate import unique_cows
from pycowview.metrics import interaction_time
from onmi import onmi
import networkx as nx
%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib as mpl
import itertools
import os
import community
from collections import defaultdict
import progressbar
import random

# Clique Percolation algorithm
def community_detection_PC(i,pos,G_AM):
    # Remove the nodes whose degree is zero
    nodes_removed = [node for node,degree in dict(G_AM.degree()).items() if degree == 0]
    G_AM.remove_nodes_from(nodes_removed)
    
    #Start percolation clique algorithm
    #listcommunities_PC = nx.algorithms.community.k_clique_communities(G_AM,3)
    communities_PC_frozen = list(nx.algorithms.community.k_clique_communities(G_AM,3))
    communities_PC = [set(x) for x in communities_PC_frozen]
    len_PC = len(communities_PC)
    print(len_PC)
    #print('Modularity',nx.algorithms.community.quality.modularity(G_AM,communities_PC))
    # Give the nodes in the graph an attribute:community_PC
    # The erial number of communities starts from 1
    community_dict_PC = defaultdict(list)  
    community_num_PC = 1
    for community_PC in communities_PC:
        for character_PC in community_PC:
            community_dict_PC[character_PC].append(community_num_PC)
            nx.set_node_attributes(G_AM, community_dict_PC, 'community_PC')
        community_num_PC += 1
    
    # Part for plotting and saving figures

    # compute graph layout
    #pos = nx.kamada_kawai_layout(G_AM)
    #pos = nx.random_layout(G_AM) 
    #pos = nx.circular_layout(G_AM)  
    #pos = nx.shell_layout(G_AM)
    pos = nx.spring_layout(G_AM, k=0.2, pos=None, fixed=None, iterations=50, threshold=0.0001, weight='weight', scale=1, center=None, dim=2, seed=7) 

    # image size
    plt.figure(figsize=(30, 30)) 
    nx.draw_networkx_nodes(G_AM, pos, node_size = 100,node_color = 'black',alpha = 0.1)
    nx.draw_networkx_edges(G_AM, pos, alpha=0.01)
    nx.draw_networkx_labels(G_AM, pos, alpha= 0.5, font_color='grey')
    # Colormap for plotting
    color_PC = 0
    random.seed(7)
    total_colors = list(mpl.colors.get_named_colors_mapping())
    total_colors.remove('black')
    color_map_PC = random.sample(total_colors,len_PC)
    #color_map_PC = ['red', 'blue','yellow','purple','pink','green','pink','brown','cyan','gold','olive','navy','hotpink','tomato','crimson','azure','peru']
    for community_PC in communities_PC:
        nx.draw_networkx_nodes(G_AM, pos , nodelist = community_PC, node_size = 200, node_color = color_map_PC[color_PC])
        nx.draw_networkx_edges(G_AM, pos ,edgelist = list(itertools.chain.from_iterable([list(G_AM.edges(node)) for node in community_PC])) ,edge_color = color_map_PC[color_PC], alpha = 0.5)
        color_PC += 1

    plt.savefig('./community/PC/Day%d.png'%i)    
    #plt.show()
    plt.close()
    
    return communities_PC

# unweighted Louvain
def community_Louvain(i,G):
    #print('This is the result of day %d'%(i+1))
    
    # Remove the nodes whose degree is zero
    nodes_removed = [node for node,degree in dict(G.degree()).items() if degree == 0]
    G.remove_nodes_from(nodes_removed)
    print(len(nodes_removed),'nodes whose degree is zero are removed')
    
    # Louvain algorithm
    partition = community.best_partition(G,randomize=False)
    num_communities = max(partition.values())
    
    # create a dict object:{community1:[nodelist],community2:[nodelist],......}
    # community1:[nodelist] is a tuple
    communities_Louvain = defaultdict(list) 
    for k, v in partition.items():
        communities_Louvain[v].append(k)    
    np.save('./community/Louvain/Day_%d_Louvain_Unweighted_communities.npy'%(i+1), communities_Louvain)
    
    #read the dict from file
    #communities_Louvain = np.load('./community/Louvain/Day_%d_Louvain_Unweighted_communities.npy', allow_pickle='TRUE')
    #print(communities_Louvain)

    num_communities = max(partition.values())
    len_Louvain = len(communities_Louvain)
    #communities_Louvain_modularity = [set(x) for x in communities_Louvain.values()]
    
    #print(communities_Louvain_modularity)
    print('Modularity:',nx.algorithms.community.quality.modularity(G,communities_Louvain.values()))
    print('max No. of community:',num_communities)
    print('num of communities:',len_Louvain)

    # Colormap for plotting
    color_Louvain = 0
    random.seed(7)
    total_colors = list(mpl.colors.get_named_colors_mapping())
    total_colors.remove('black')
    color_map_Louvain = random.sample(total_colors,len_Louvain)

    # Plot the figure
    plt.figure(figsize=(15, 15))  # image size
    pos = nx.fruchterman_reingold_layout(G, scale = 1) # position of nodes
    degree_dict = dict(G.degree())
    nx.draw_networkx(G, pos, node_size=5,width=0.05, alpha=1, with_labels=False)
    for community_Louvain in communities_Louvain.items():
        
        node_list = community_Louvain[1]
        edge_list = list(itertools.chain.from_iterable([list(G.edges(node)) for node in node_list]))
        label_list = {}
        for node in node_list:
            #set the node name as the key and the label as its value 
            label_list[node] = node 
        community_degree_dict = {key: value for key, value in degree_dict.items() if key in node_list}
        node_size_list = [d*20 for d in community_degree_dict.values()]
        
        nx.draw_networkx_nodes(G, pos , nodelist = node_list, node_size = node_size_list, node_color = color_map_Louvain[color_Louvain],alpha = 0.7)
        nx.draw_networkx_edges(G, pos , edgelist = edge_list, edge_color = color_map_Louvain[color_Louvain],alpha = 0.2)
        nx.draw_networkx_labels(G, pos, label_list, font_size = 8, font_color = color_map_Louvain[color_Louvain],alpha = 0.7)
        color_Louvain += 1
    plt.savefig('./community/Louvain/Day%d_Unweighted_Community.png'%(i+1))
    plt.show()
    
    return nodes_removed, communities_Louvain, partition
    
# Girvan-Newman community detection
def community_detection_GN(i,pos,G_AM):
    # Remove the nodes whose degree is zero
    nodes_removed = [node for node,degree in dict(G_AM.degree()).items() if degree == 0]
    G_AM.remove_nodes_from(nodes_removed)

    # Start GN algorithm
    comp = nx.algorithms.community.girvan_newman(G_AM)

    # limit the number of communities, k =20 communities we assume
    k = 20
    limited = itertools.takewhile(lambda c: len(c) <= k, comp)
    communities_GN = list(limited)[-1]
    
    print(nx.algorithms.community.quality.modularity(G_AM,communities_GN))

    # Give the nodes in the graph an attribute:community_GN
    # The erial number of communities starts from 1
    community_dict_GN = defaultdict(list)
    community_num_GN = 1
    for community_GN in communities_GN:
        for character_GN in community_GN:
            community_dict_GN[character_GN].append(community_num_GN)
            nx.set_node_attributes(G_AM, community_dict_GN, 'community_GN')
        community_num_GN += 1

    # Part for plotting and saving figures

    # compute graph layout
    #pos = nx.kamada_kawai_layout(G_AM)
    #pos = nx.random_layout(G_AM) 
    #pos = nx.circular_layout(G_AM)  
    #pos = nx.shell_layout(G_AM)
    #pos = nx.spring_layout(G_AM, k=0.2, pos=None, fixed=None, iterations=50, threshold=0.0001, weight='weight', scale=1, center=None, dim=2, seed=7) 

    # image size
    plt.figure(figsize=(30, 30)) 
    nx.draw_networkx_nodes(G_AM, pos, node_size = 100,node_color = 'black',alpha = 1)
    nx.draw_networkx_edges(G_AM, pos, alpha=0.2)
    nx.draw_networkx_labels(G_AM, pos, alpha=0.5)
    # Colormap for plotting
    color_GN = 0
    color_map_GN = ['red', 'blue', 'yellow', 'purple',  'pink', 'green', 'pink','brown','cyan','gold','red', 'blue', 'yellow', 'purple',  'pink', 'green', 'pink','brown','cyan','gold']
    for community_GN in communities_GN:
        nx.draw_networkx_nodes(G_AM, pos , nodelist = community_GN, node_size = 100, node_color = color_map_GN[color_GN])
        nx.draw_networkx_edges(G_AM, pos ,alpha = 0.02)
        color_GN += 1

    plt.savefig('./community/GN/Day%d.png'%i)    
    #plt.show()
    plt.close()
    
    return communities_GN
