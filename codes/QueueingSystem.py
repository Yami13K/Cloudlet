# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 21:16:26 2021

@author: Eng.Mohammad Sakka
"""
import numpy as np
import  Server
class QueueingSystem:
    
    #%% constructor
    def __init__(self,numberOfServers,B):
        self._cloudExecutionRate = 8 * 2**30 # line per second
        self._totalNumberOfServedTasks = 0
        self._totalNumberOfRefusedTasks = 0
        self._totalServingTime = 0
        self._numberOfTasksInQueue = 0
        self._totalWaitTime = 0
        self._numberOfServers = numberOfServers
        self._numberOfArrivedTasks = 0
        self._numberOfCurrentTaskInSystem = 0
        self._B = B # internet delay in [second]
        self._servers = []
        for si in range(self._numberOfServers):
            s = Server.Server(si)
            self._servers.append(s)
        #%% function serviceTask
    def serviceTask(self,task,timeCounter,performanceLogger):
        self._numberOfArrivedTasks+=1
        self._numberOfCurrentTaskInSystem+=1
        assigned = False
        assigned,serverId,task = self.assigneTaskToServer(task,timeCounter)
        
        if assigned:
            performanceLogger.pickWaitDelayOfTask(timeCounter,task.waitingTime)
        #while not assigned:
         #   assigned,serverId = self.assigneTaskToServer(task)
        if assigned:
            execTime,execEnergy,renting = self._servers[serverId[0]].executeTask(task,timeCounter)
            return assigned,execTime,execEnergy,renting
        else:
            return assigned,0,0,0
     #%% function serversFree
    def serversFree(self,timeCounter):
        for si in range(self._numberOfServers):
            if not self._servers[si].getIsIdle():
                taskLenOfRows = self._servers[si].getCurrentTask().numberOfLines
                if (timeCounter-(1/self._servers[si].getServiceRate())*\
                    taskLenOfRows)>=(1/self._servers[si].getServiceRate()):
                    self._servers[si].releaseTask()
        

        #%% function assigneTaskToServer
    def assigneTaskToServer(self,task,timeCounter):
        isIdleList = []
        for si in range(self._numberOfServers) :
            isIdleList.append(self._servers[si].getIsIdle())
            isIdleList = [int(ii) for ii in isIdleList ]
            isIdleList = np.array(isIdleList)
            idleServersIds = np.argwhere(isIdleList==1)
            if len(idleServersIds)>0: # if there is idle servers
                selectedServerId = np.random.randint\
                (low=0,high=len(idleServersIds))
                selectedServerId = idleServersIds[selectedServerId]
                self._servers[selectedServerId[0]].updateState(False)
                self._numberOfCurrentTaskInSystem -=1 
                self._numberOfTasksInQueue -=1
                self._servers[selectedServerId[0]].assigneTask(task)
                task.waitingTime = timeCounter - task.momentOfGeneration
                return True,selectedServerId,task
            else:
                return False,np.nan,task
 #%%  function sendTaskToCloud
    def sendTaskToCloud(self,task):
        internetDelay = task.getDataPucketSize()*(1/self._B)
        execTime = task.numberOfLines * (1/self._cloudExecutionRate)
        delay = internetDelay + execTime
        return delay
#%% end   