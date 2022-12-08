# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 15:35:20 2021

@author: mhdsq
"""
import numpy as np
import itertools
import Task
class User:
    __iterId = itertools.count()
    #%%
    def __init__(self,vector,isInitial):
        newid = next(User.__iterId)
        self.__id = newid
        if isInitial:
            self.__position = np.random.uniform(low=(0,0),high=(vector[0],vector[1]),size=2)   
        else:
            self.__position = vector
        #averageSending = np.random.uniform(0.1,3)
        self.taskSendingRate = np.random.normal(3,1) # task per timeUnit
        self.__base_station_id = np.nan
        self.__base_station_Loc = np.nan
        self.__nextTimeOfSendingTask = np.random.poisson(lam=self.taskSendingRate)
        self.transPow = 0.1 # [W]
        self.__serviceRate = 2* 2**30 # in [line per second]
        self.__effectiveSwitchedCapacity = 5*(10**-27)
        self.averageDataSize = np.random.uniform(low=200*1024,high=500*1024)
        self.averageCompDemand = np.random.uniform(low=1000,high=2000) 
     #%% get functions
    def getId(self):
        return self.__id
     
    def getLocation(self):
        return self.__position
    
    def getNextTimeOfSendingTask(self):
        nextTime =  self.__nextTimeOfSendingTask
        self.__nextTimeOfSendingTask = self.__nextTimeOfSendingTask + np.random.poisson(lam=self.taskSendingRate)
        return nextTime
    #%%
    def Move(self):
        self.__position[0] = self.__position[0] + np.random.normal(1.5,0.5)
        self.__position[1] = self.__position[1] + np.random.normal()
    #%%
    def assigneTobase_station(self,base_stationid,bsLoc):
        self.__base_station_id = base_stationid
        self.__base_station_Loc = bsLoc
   #%%
    def sendTask(self,timeCounter,averageDataSize,averageCompDemand):
        T = Task.Task(timeCounter,averageDataSize,averageCompDemand)
        bsPos = self.__base_station_Loc
        userPos = self.__position
        distTobase_station = np.linalg.norm(userPos - bsPos)
        #wirelessDelay = self.__wirelessDelayPerMeter * distTobase_station * (1/self.__wirelessDataRate)
        return T,self.__base_station_id,distTobase_station
    
    #%%
    def generateTask(self,timeCounter,averageDataSize,averageCompDemand):
        T = Task.Task(timeCounter,averageDataSize,averageCompDemand)
        return T
    
    def executeTask(self,T,timeCounter):
        E = self.__effectiveSwitchedCapacity * (self.__serviceRate**2) * \
            T.numberOfLines
        delay = (1/self.__serviceRate)*T.numberOfLines
        return E,delay
#%% end