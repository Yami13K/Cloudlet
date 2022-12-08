# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 22:40:47 2021

@author: mhdsq
"""
from QueueingSystem import QueueingSystem
 
class Cloudlet(QueueingSystem):  
    #%% constructor
    def __init__(self,basestation_id,serversNum,lamdaMax,B):
        super().__init__(serversNum,B)
        self.__basestation_id = basestation_id
        self.__queue = []
        self.__lamdaMax = lamdaMax
        self.__numInQ = 0
        self._numberOfTasksInQueue = self.__numInQ
 
    #%% get functions
    def getBsId(self):
        return self.__basestation_id
    
    def getLenOfQueue(self):
        return(len(self.__queue))
  #%% for later use  
    def updateAssignedBS(self):
        pass
    
    #%% function assigneToCloudlet
    def assigneToCloudlet(self,timeCounter,task,performanceLogger):
        if len(self.__queue)<=self.__lamdaMax:
            self.enQueue(task)
            performanceLogger.pickServedTasks(timeCounter)
        else:
            delay = self.sendTaskToCloud(task)
            self._totalNumberOfRefusedTasks+=1
            performanceLogger.pickRefucedTasks(timeCounter)
            performanceLogger.pickDelayOfSendToCloud(timeCounter,delay)
    
    
    #%% function enQueue
    def enQueue(self,task):
        
            self.__queue.append(task)
            self.__numInQ = len(self.__queue)
            self._numberOfTasksInQueue = self.__numInQ
    
    #%% function serviceTasks
    def serviceTasks(self,timeCounter,performanceLogger):
        task = self.__queue[0]
        served,execTime,execEnergy,renting = super().serviceTask(task,timeCounter,performanceLogger)
        if served:
            self._totalNumberOfServedTasks+=1
            self._totalServingTime +=  execTime 
            self.deQueue()
            return served,execTime,execEnergy,renting
        else:
            return served,0,0,0
        
    #%% function deQueue
    def deQueue(self):
        
        self.__queue.pop(0)
        self.__numInQ -=1
        self._numberOfTasksInQueue = self.__numInQ
#%% end   