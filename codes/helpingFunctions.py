# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 16:23:32 2021

@author: mhdsq
"""
# Python program to convert Adjacency matrix
# representation to Adjacency List
 
from collections import defaultdict
# converts from adjacency matrix to adjacency list
    
def convertAdjMatToEdgesList(a):
    adjList = defaultdict(list)
    for i in range(len(a)):
        for j in range(len(a[i])):
                       if a[i][j]== 1:
                           adjList[i].append(j)
    return adjList
 
