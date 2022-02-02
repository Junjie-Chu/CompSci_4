# Introduction to different functions
Example of each fucntion could be found in example folder.
If the intro is not enough, there are some more detailed comments in the source code.
## utilize_general_CommunityDetectionMethods_unweighted.py
1. Clique Percolation algorithm：community_detection_PC(i,pos,G_AM)
2. Unweighted Louvain: community_Louvain(i,G)
3. Girvan-Newman community detection: community_detection_GN(i,pos,G_AM)  

*i is the ith day. pos is the layout. G/G_AM is the graph from adjacency matrix.  
return is the community partition of that day.*

## utilize_general_CommunityDetectionMethods_weighted.py
1. Weighted Louvain: community_Louvain(i,G)

*i is the ith day. pos is the layout. G/G_AM is the graph from adjacency matrix.  
return is the community partition of that day.*
## utilize_general_CommunityMeasurements.py
1.  Function for NMI: compute_NMI(p1,p2)  
    *p1,p2 are the partitions of 2 days, how to get them could be seen in the examples.*
2.  Function for random simulation: create_rand_adjacency(day)
    *create binary/weighted adjacency matrices of random simulation. The matrices have the same density of that input day.*
3. Function for simularity of graph.
4. Function for showing nodes of highest N degree.  

***Note: The examples of 1 and 2 could be found in cow_weighted_Louvain_all_area.ipynb. The examples of 3 and 4 could be found in cow_unweighted_Louvain.ipynb.***

## utilize_general_unweighted.py
1. This function will get the path of each csv file: findAllFile(base).  
    *base is the path of the folder.*
2. Load matrices and convert them into unweighted graphs: time_matrix_to_graph(tm_folder,cl_folder).
    * *Input is the folders where the time matrix and cowlist are saved.*
    * *Output is a list which consists of 14 dictionaries. The structure of a dictionary: Cowlist, TimeMatrix, AajacencyMatrix_binary, Unweighted_Graph.*
      
***Note: The examples of 1 and 2 could be found in almost all .ipynb files.***
## utilize_general_weighted.py
Very similar to the above functions, but this file is for weighted version.
