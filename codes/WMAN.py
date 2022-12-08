# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 15:05:12 2021

@author: Eng.Mohammad Sakka
"""
import numpy as np
import User
import BS
import Cloudlet
import PerformanceLogger
from dijkstar import Graph, find_path

class WMAN:
    #%% constructor 
    def __init__(self,areaDims,numberOfBSs,initUsersRange,numberOfCloudlets,numberOfServersPerCloudlet\
                 ,BScommDataRate,wirelessDelayPerMeter,wirelessDataRate,dataPucketSize,lamdaMax,B,deltaT):
        self.deltaT = deltaT
        self.__X = (np.zeros(numberOfBSs)) # cloudlet assognement vector
        self.__X = self.__X>0
        cloudletsInds = np.random.randint(low=0,high=numberOfBSs,size = numberOfCloudlets)
        self.__X[cloudletsInds] = bool(1)
        self.__isZSet = bool(0)
        
        self.__mapDims = areaDims # area dimencions
        self.__BSNum = numberOfBSs # number of base stations
        #self.__initialUsersNum = initUsersRange # number of initial users range
        self.__cloudletsNum = numberOfCloudlets # number of cloudlets
       # compute the cloudlet setting ratio based on the numberOfCloudlets/numberOfBaseStation
        #cloudletsRatio = self.__cloudletsNum/self.__BSNum
        # generating random BSs graph
        # first we generate unweighted graph to determine the connections 
        # between the BSs then the weighted graph determined by position of each BS
        self.__BSGraph = np.random.randint(low=0,high=2,size=(numberOfBSs,numberOfBSs))
        # make the matrix symmitric
        self.__BSGraph = np.maximum( self.__BSGraph,self.__BSGraph.transpose())
        self.__initialUsersNum = np.random.randint(low=initUsersRange[0],high=initUsersRange[1])
        self.__currentNumberOfUsers = self.__initialUsersNum
        self.__Z = np.random.uniform(low=0,high=1,size=(self.__initialUsersNum,numberOfCloudlets))
        for i in range(self.__Z.shape[0]):
            self.__Z[i,:] = self.__Z[i,:]/np.sum(self.__Z[i,:])
        self.__users = [] # list of all users 
        self.__BS = [] # list of all base stations
        self.__cloudlets = [] # list of all cloudlets
        self.__performanceLogger = PerformanceLogger.PerformanceLogger() # performance logger object
        # generate the initial users
        initial = True # this is initial user
        for i_usr in range(self.__initialUsersNum):
            u = User.User(areaDims,initial)
            self.__users.append(u)
        
        # generate BSs objects
        for i_bs in range(self.__BSNum):
            if self.__X[i_bs]:
                isCloudlet = 1 
            else:
                isCloudlet = 0
            a = BS.BS(i_bs, areaDims, BScommDataRate, self.__BSGraph, isCloudlet, wirelessDelayPerMeter, wirelessDataRate)
            self.__BS.append(a)
            # create the cloudlets objects
            if isCloudlet==1:
                cld = Cloudlet.Cloudlet(a.getId(),numberOfServersPerCloudlet,lamdaMax,B)
                self.__cloudlets.append(cld)
             
        # initialize delay matrix
        self.__delayMatrix = np.zeros((self.__BSNum,self.__BSNum))
        
        # initialize distance matrix
        self.__distMatrix = np.zeros((self.__BSNum,self.__BSNum))
        
        #  Matrix (D)
        self.__D = np.zeros((self.__BSNum,self.__BSNum))
        
        # note: BScommDelay is the delay in [second per meter]
        
        # calculate delayMatrix and dist matrices
        for i in range(self.__BSNum):
            for j in range(self.__BSNum):
                if self.__BSGraph[i][j]==0:
                    self.__distMatrix[i][j] = None
                    self.__delayMatrix[i][j] = None
                else: # if self.__BSGraph[i][j]==1
                    self.__distMatrix[i][j] = 1 # set as one and considered as 
                    # un weighted graph because we neglected the distance delay 
                    # and only considered the routing delay
                   
        
        # calculate D matrix using Dijkstra Algorithm
        # convert the adjaMat to edgesList
        # edgesList = convertAdjMatToEdgesList(self.__BSGraph)
        graph = Graph() # for using dijkstra algorithm
        # building the graph
        for ia in range(self.__BSNum):
            for ja in range(self.__BSNum):
                if self.__BSGraph[ia][ja]==1:
                    graph.add_edge(ia, ja, 1)
                
        # building D matrix using Dijkstra
        for ia in range(self.__BSNum):
            for ja in range(self.__BSNum):
                path = find_path(graph, ia, ja)
                delay = path.total_cost
                self.__D[ia][ja] = delay
                self.__delayMatrix[i][j] = (1/BScommDataRate)*dataPucketSize*delay
    #%% (get) functions
    def getAreaDims(self):
        return self.__mapDims
    
    def getBSsGraph(self):
        return self.__BSGraph
    
    def getBSs(self):
        return self.__BS
    
    def getUsers(self):
        return self.__users
    
    def getCloudlets(self,timeCounter):
        return self.__cloudlets
    
    def getPerformanceLogger(self):
        return self.__performanceLogger
    
    def getZ(self):
        return self.__Z
    def getX(self):
        return self.__X
    #%% function set_X
    def set_X(self,X):
        self.__X = X
        for i_bs in range(self.__BSNum):
            if self.__X[i_bs]:
                self.__BS[i_bs].setAsCloudlet(1)
            else:
                self.__BS[i_bs].setAsCloudlet(0)
    #%% function set_Z
    def set_Z(self,Z):
        self.__Z = Z
        self.__isZSet = bool(1)
     #%% function update current number of users  
    def updateCurrentNumberOfUsers(self):
        self.__currentNumberOfUsers = len(self.__users)
    #%% function deleteUser
    def deleteUser(self,timeCounter):
        if (timeCounter % self.deltaT) != 0 or timeCounter==0:
            self.updateCurrentNumberOfUsers()# do nothing
        else:
            toDel = []
            for iu in range(len(self.__users)):
                pos = self.__users[iu].getLocation()
                dim1 = self.__mapDims[0]
                dim2 = self.__mapDims[1]
    
                if ((pos[0]<0 or pos[0]>dim1) or (pos[1]<0 or pos[1]>dim2)):
                    toDel.append(iu)
           
            for ele in sorted(toDel, reverse = True):
                del self.__users[ele]
          
            self.updateCurrentNumberOfUsers()
     
      #%% function addUser  
    def addUser(self,timeCounter):
        if (timeCounter % self.deltaT) != 0 or timeCounter==0:
            # do nothing
            self.updateCurrentNumberOfUsers()
        else:
            dim1 = self.__mapDims[0]
            dim2 = self.__mapDims[1]
            sideOfUserEntering = np.random.randint(low=1,high=5)
            newUsrPos = np.zeros(2)
            if sideOfUserEntering == 1:
                newUsrPos[0] = 0
                newUsrPos[1] = np.random.uniform(low=0,high=dim2)
            elif sideOfUserEntering == 2:
                newUsrPos[0] = dim1
                newUsrPos[1] = np.random.uniform(low=0,high=dim2)
            elif sideOfUserEntering ==3:
                newUsrPos[0] = np.random.uniform(low=0,high=dim1)
                newUsrPos[1] = dim2
            else: # sidOfUserEntering ==4
                newUsrPos[0] = np.random.uniform(low=0,high=dim1)
                newUsrPos[1] = 0
                
            
            # creating the new user object
            initial = False
            usr = User.User(newUsrPos,initial)
            self.__users.append(usr)
            self.updateCurrentNumberOfUsers()
    #%% function assigneUserToBS
    def assigneUserToBS(self):
        currNumOfUsrs = self.__currentNumberOfUsers
        BSsNum = self.__BSNum
        usersBSsDistAdjaMat = np.zeros((currNumOfUsrs,BSsNum))
        for iu in range(currNumOfUsrs):
            userPos = self.__users[iu].getLocation()
            for ip in range(BSsNum):
                bsPos = self.__BS[ip].getLocation()
                dist = np.linalg.norm(userPos-bsPos)
                usersBSsDistAdjaMat[iu][ip] = dist
            # end for ip
        # end for bs
        # assigne the users
        for iu in range(currNumOfUsrs):
            row = usersBSsDistAdjaMat[iu,:]
            bsIdx = row.argmin(0)
            self.__users[iu].assigneTobase_station(bsIdx,self.__BS[bsIdx].getLocation())
        # end for iu
    
    # end function assigneToBS
    #%% function send_receive_tasks
    def  send_receive_tasks(self,timeCounter,performanceLogger):
        
        for iu in range(self.__currentNumberOfUsers):
            if self.__users[iu].getNextTimeOfSendingTask() < timeCounter:
                continue
            else:
                # send or not send
                shrinked_Z = self.__Z[iu]
                probOfLocalExec = 1 - np.sum(shrinked_Z)
                shrinked_Z = np.hstack((shrinked_Z,probOfLocalExec))
                p = shrinked_Z/sum(shrinked_Z)
                s = sorted(range(len(p)), key=lambda k: p[k])
                p = p[s]
                cummulative_p = np.zeros(len(p))
                for i in range(len(p)):
                    cummulative_p[i] = np.sum(p[:i+1])
                randomVal = np.random.uniform()
                selected = np.nonzero(randomVal<cummulative_p)
                selected = selected[0]
                while np.size(selected) != 1:
                    selected = selected[0]
                try:
                    cond = selected[0]==(len(shrinked_Z)-1)
                except:
                    cond = selected==(len(shrinked_Z)-1)
                    
                if cond:
                        distenationCloudlet = np.nan
                        task = self.__users[iu].generateTask(timeCounter,\
                            self.__users[iu].averageDataSize,self.__users[iu].averageCompDemand)
                        userExecEnergy,userExecDelay = \
                            self.__users[iu].executeTask(task,timeCounter)
                        
                        performanceLogger.pickDelayOfUserExec(timeCounter,userExecDelay)
                        performanceLogger.pickUserExecEnergy(timeCounter,userExecEnergy)
                else: 
                    task,bsId,distToBS = self.__users[iu].sendTask(timeCounter,\
                     self.__users[iu].averageDataSize,self.__users[iu].averageCompDemand)
                    wirelessDelay = self.__BS[bsId].getWirelessDelayPerMeter()\
                    * distToBS * (1/self.__BS[bsId].getWirelessDataRate())
                    wirelessEnergy = wirelessDelay * self.__users[iu].transPow *\
                         task.dataPucketSize
                    performanceLogger.pickSendingEnergy(timeCounter,wirelessEnergy)
                    performanceLogger.pickWirelessDelay(timeCounter,wirelessDelay)
#                self.__users[iu].workload.append(task)
                    performanceLogger.pickArrivedTask(timeCounter)
                    distenationCloudlet,delayOfRoutig = self.__BS[bsId].receiveTask\
                            (task,self.__cloudlets,self.__D,self.__delayMatrix,\
                             self.__isZSet,self.__Z,self.__users[iu].getId())
                    self.__cloudlets[distenationCloudlet].assigneToCloudlet\
                        (timeCounter,task,self.__performanceLogger)
                    performanceLogger.pickDelayOfRouting(timeCounter,delayOfRoutig)
                    
        #%% function serviceTasks
    def serviceTasks(self,timeCounter,performanceLogger):
        for ic in range(len(self.__cloudlets)):
            if self.__cloudlets[ic].getLenOfQueue() > 0:
                served,execTime,execEnergy,renting =  self.__cloudlets[ic].serviceTasks(timeCounter,performanceLogger)
                if served:
                    performanceLogger.pickExecTime(timeCounter,execTime)
                    performanceLogger.pickExecEnergy(timeCounter,execEnergy)
                    performanceLogger.pickRenting(timeCounter,renting)
    
    #%% function releasingEndedTasks
    def releasingEndedTasks(self,timeCounter):
        for ic in range(len(self.__cloudlets)):
            self.__cloudlets[ic].serversFree(timeCounter)
    

    #%%  function: "Doing my routine"
    def DoingMyRoutine(self,timeCounter,isZset):
        self.__isZset = isZset
        # move the users
        for u in self.__users:
            u.Move() 
        # delete the users that were exceed the area boundary
        self.deleteUser(timeCounter)
        self.addUser(timeCounter)
        # assigning each user to the approporiate base station
        self.assigneUserToBS()
        # allow the users to send them tasks to the BSs and recieve the tasks
        # in the base stations
        self.send_receive_tasks(timeCounter,self.__performanceLogger)
        # service the recieved and queued tasks
        self.serviceTasks(timeCounter,self.__performanceLogger)
        # releasing the completed tasks
        self.releasingEndedTasks(timeCounter)
        # compute the measures

        
        self.__performanceLogger.findSendEnergy_TS(timeCounter)
        self.__performanceLogger.findUserExecEnergy_TS(timeCounter)
        self.__performanceLogger.findTotalEnergy_TS(timeCounter)
        self.__performanceLogger.findRenting_TS(timeCounter)
        
        self.__performanceLogger.findSTR_TS(timeCounter)
        self.__performanceLogger.findRTR_TS(timeCounter)
        self.__performanceLogger.findArrivedTask_TS(timeCounter)
        self.__performanceLogger.calc_averageWaitDelayOfTasks_timeSeries(timeCounter)
        self.__performanceLogger.calc_averageWirelessDelayOfTasks_timeSeries(timeCounter)
        self.__performanceLogger.calc_averageRoutingDelayOfTasks_timeSeries(timeCounter)
        self.__performanceLogger.calc_averageSendToCloudDelayOfTasks_timeSeries(timeCounter)
        self.__performanceLogger.calc_averageExecDelayOfTasks_timeSeries(timeCounter)
        self.__performanceLogger.calc_averageUsersExecDelayOfTasks_timeSeries(timeCounter)
        self.__performanceLogger.findSRT_TS(timeCounter)
        # print the values
        # print("SRT: ",self.__performanceLogger.getSRT_TS())
        # print("TE: ",self.__performanceLogger.getTotalEnerg_TS())
        # print("EE: ",self.__performanceLogger.getExecEnerg_TS())
        # print("SE: ",self.__performanceLogger.getSendingEnerg_TS())
        # print("AT: ",self.__performanceLogger.getArrivedTasks_TS())
        # print("STR: ",self.__performanceLogger.getSTR_TS())
        # print("RTR: ",self.__performanceLogger.getRTR_TS())
        # print("UET: ",self.__performanceLogger.getUserExecDelay_TS())
        # print("UEE: ",self.__performanceLogger.getUserExecEnergy_TS())
        #%% function return all measures
        def returnAllMeasures(self,timeCounter):
            systemResponceTime = self.__performanceLogger.getSRT_TS()[timeCounter]
            energyConsumption = self.__performanceLogger.getTotalEnerg_TS()[timeCounter]
            return systemResponceTime,energyConsumption
        
            
    #%% end