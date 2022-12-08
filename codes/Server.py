# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 21:57:28 2021

@author: Eng.Mohammad Sakka
"""
import numpy as np
class Server:
    #%% constructor
    def __init__(self,Id):
        self.__id = Id
        self.__isIdle = True # server state
        self.__numberOfServedTasks = 0
        self.__serviceRate = 4* 2**30 # in [line per second]
        self.__sumOfServicesTimes = 0 # accumulator along all tasks
        #self.__sumOfWaitTimes = 0 # accumulator along all tasks
        self.__timeOfStartExec = np.inf
        self.__effectiveSwitchedCapacity = 5*(10**-27)
        self.__rentingRate = 10 # [$/sec]
    #%% function assigneTask
    def assigneTask(self,task):
        self.__currentTask = task
    #%% get functions
    def getCurrentTask(self):
        return self.__currentTask
    def getServiceRate(self):
        return self.__serviceRate
    def getIsIdle(self):
        return self.__isIdle
    def getStartExecTime(self):
        return self.__timeOfStartExec
    def getRentingRate(self):
        return self.__rentingRate
    #%%function updateState
    def updateState(self,state): # update isIdle attribute
        self.__isIdle = state
    #%% function executeTask
    def executeTask(self,task,timeCounter): # execute task
        task.executed = True
        #time.sleep(self.__serviceTime) 
        self.__timeOfStartExec = timeCounter
        self.__numberOfServedTasks +=1
        #self.__sumOfServicesTimes +=  self.__serviceTime
        execEnergy = self.__effectiveSwitchedCapacity * (self.__serviceRate**2)\
            * task.numberOfLines
        return (1/self.__serviceRate)*task.numberOfLines,execEnergy,\
            (1/self.__serviceRate)*task.numberOfLines * self.__rentingRate
    #%% function releaseTask
    def releaseTask(self): # release the task after execution
        self.__isIdle = True
        return True
#%% end