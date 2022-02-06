library(network)
library(ergm)
library(igraph)
library(intergraph)
library(statnet)
library(sna)
library(ggplot2)

rm(list = ls())
set.seed(Sys.time())
setwd("~/Github")
#Download the adjacency matrix 
adj_mat_temp <- read.csv("Adj_data/ADJ_20201028T000000UTC.csv",header=FALSE)
Node_list_temp <- read.csv("Cows/Cow_list_20201028T000000UTC.csv")
adj_mat <- as.matrix(adj_mat_temp)
Node_list <- as.matrix(Node_list_temp)
diag(adj_mat)=0

g1 <- graph_from_adjacency_matrix(adj_mat, mode="undirected")
nw1 <- asNetwork(g1)
globtrans<-transitivity(g1, type="global")
d0=degree(nw1)
t1=numeric(1000)
for (i in 1:1000) {
set.seed(Sys.time())
random_network=sample_degseq(d0)
random_network=simplify(random_network)

t1[i]=transitivity(random_network, type="global") # global transitivity
}
mean(t1)
sd(t1)
t1[9]
t1[300]

