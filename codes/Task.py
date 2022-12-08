# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 16:12:21 2021

@author: mhdsq
"""
import numpy as np
import itertools
class Task:
    #%% those variables are to made as input values
    #dataPucketSize = 1024 # [bit]
    #numberOfLines = 10
    #%% incremental ids
    __iterId = itertools.count()
    #%% constructor
    def __init__(self,timeCounter,averageDataSize,averageCompDemand):
        newid = next(Task.__iterId)
        self.__id = newid
        self.executed = False
        self.toRemove = False
        self.momentOfGeneration = timeCounter
        self.waitingTime = 0
        self.dataPucketSize = np.random.exponential(averageDataSize)
        self.numberOfLines = np.random.exponential(averageCompDemand)
    #%% get functions
    def getDataPucketSize(self):
        return self.dataPucketSize
    def getId(self):
        return self.__id
 #%%    end