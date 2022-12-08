# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 16:04:57 2021

@author: eng. mohammad sakka
"""
import numpy as np
class BS:
#%% constructor
    def __init__(self,Id,areaDims,commDelay,BSsGraph,isCloudlet,wirelessDelayPerMeter,wirelessDataRate):
        self.__id = Id
        self.__isCloudlet = isCloudlet
        self.__communicationDelay = commDelay
        self.__location = np.random.uniform(low=(0,0),high=(areaDims[0],areaDims[1]),size=2)
        self.__assosiatedBSsIds = np.array(np.nonzero(BSsGraph[Id,:] == 1))
        self.__numberOfAssosiatedBSs = len(self.__assosiatedBSsIds)
        #self.__linksLengths = []
        self.__wirelessDelayPerMeter = wirelessDelayPerMeter
        self.__wirelessDataRate = wirelessDataRate
        
    #%% function setAsCloudlet
    def setAsCloudlet(self,isCloudlet):
        self.__isCloudlet = isCloudlet
    #%% get functions
    def getWirelessDelayPerMeter(self):
        return self.__wirelessDelayPerMeter
    
    def getWirelessDataRate(self):
        return self.__wirelessDataRate
    
    def getId(self):
        return self.__id
                 
    def getLocation(self):
        return self.__location
    
    def getAssosiatedBSsIds(self):
        return self.__assosiatedBSsIds
    
    def getIsBScloudelet(self):
        return self.__isCloudlet
    
    #%% function receiveTasks
    def receiveTask(self,task,cloudlets,Dmat,delayMat,isZSet,Z,user_id):
        distenationCloudlet,delay = self.routeToCloudlet(task,cloudlets,Dmat,\
                                                         delayMat,isZSet,Z,user_id)
        return distenationCloudlet,delay
    
    #%% function routeToCloudlet
    def routeToCloudlet(self,task,cloudlets,Dmat,delayMat,isZSet,Z,user_id):
        cloudletsIds = []
        for ic in range(len(cloudlets)):
            cloudletsIds.append(cloudlets[ic].getBsId())
        isZSet = True
        if not isZSet:
            shrinkedDmat = Dmat[:,cloudletsIds]
            shrinkedDelayMat = delayMat[:,cloudletsIds]
            row = shrinkedDmat[self.__id,:]
            row2 = shrinkedDelayMat[self.__id,:]
            distenationCloudlet =  row.argmin()
            delay = np.nanmin(row2)
        else:
            shrinked_Z = Z[user_id]
            p = shrinked_Z/sum(shrinked_Z)
            s = sorted(range(len(p)), key=lambda k: p[k])
            p = p[s]
            cummulative_p = np.zeros(len(p))
            for i in range(len(p)):
                cummulative_p[i] = np.sum(p[:i+1])
            randomVal = np.random.uniform()
            selected = np.nonzero(randomVal<cummulative_p)
            selected = selected[0]
            while np.size(selected) !=1:
                selected = selected[0]
            try:
                index = s[selected]
            except:
                index = s[selected[0]]
            shrinkedDelayMat = delayMat[:,cloudletsIds]
            row2 = shrinkedDelayMat[self.__id,:]
            si = 0
            while np.isnan(row2[index]):
                si +=1
                index = s[si]
                
            distenationCloudlet = index
            delay = row2[distenationCloudlet]
            
        return distenationCloudlet,delay
#%% end