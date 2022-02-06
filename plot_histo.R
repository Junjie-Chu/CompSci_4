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
histo=list(14)
k=16
str1="Hists/Hist_202010"
str2=toString(k)
str3="T000000UTC.csv"
result = paste(str1,str2,str3,sep="")
x <- read.csv(result,header=FALSE)
x$V1 <- as.numeric(as.character(x$V1))
plot(density(x$V1),type="l",col=1,lwd=2,xlim=c(0,30),main="",
     xlab="Edges",ylab="Cows (density)")

for (i in 1:13) {
  k=i+17
  str2=toString(k)
  result = paste(str1,str2,str3,sep="")
  x1 <- read.csv(result,header=FALSE)
  x1$V1 <- as.numeric(as.character(x1$V1))
  lines(density(x1$V1),col=i+1,lwd=2)
  }

