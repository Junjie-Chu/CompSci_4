
import numpy as np
import math as m
import networkx as nx


#The average shortest path of the network
#input: Adjacency matrix
#output: integer of the average shortest path
def Average_shortest_path(AM):
    """
        Average shortest path gets the average shortest path of the network.
        The average path needed to get from one cow to another

        :param AM: The Adjacency matrix in numpy
        :return: The average shortest path if fully connected. 0 otherwise
        """
    #AM = np.loadtxt(filename, delimiter=",")
    print(m.sqrt(AM.size))
    np.fill_diagonal(AM, 0)
    G = nx.from_numpy_matrix(AM, parallel_edges=False)
    asp=0
    if nx.is_connected(G):
        asp = nx.average_shortest_path_length(G)
    return asp

# The transitivity of the network
#input:Adjacency matrix
#output: integer of the transitivity
def Transistivity(AM):
    """
            The transitivity shows the likelyhood for the network to form groups

            :param AM: The Adjacency matrix in numpy
            :return: The transitivity of the network. between 0 and 1
            """
    #AM = np.loadtxt(filename, delimiter=",")
    np.fill_diagonal(AM, 0)
    G = nx.from_numpy_matrix(AM, parallel_edges=False)
    trans = nx.transitivity(G)
    return trans

def Connectivity(AM):
    """
            The Connectivity of the network shows returns how many edges are needed
            to be removed for the network to be disconnected

            :param AM: The Adjacency matrix in numpy
            :return: The connectivity
            """
    G = nx.from_numpy_matrix(AM,parallel_edges=False)
    connect=nx.edge_connectivity(G)
    return connect


def Algebraic_Connectivity(AM):
    """
             The algebraic connectivity of the network shows how connected the whole network is.

             :param AM: The Adjacency matrix in numpy
             :return: The algebraic connectivity
             """
    lam = LA.eig(AM)
    alg_con=lam[1]
    return alg_con

def Eigenvector_centrality(AM):
    """
               The eigenvector centrality shows how central each cow is by looking at how many connections the cow has,
               and how many connections they have

               :param AM: The Adjacency matrix in numpy
               :return: The eigenvector centrality of each node
    """
    G= nx.from_numpy_matrix(AM,parallel_edges=False)
    A=nx.eigenvector_centrality(G)
    return A

def hist_Eigenvec_cent(eigenvecs):
        plt.hist(eigenvecs)