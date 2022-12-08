# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 09:37:38 2021

@author: mhdsq
"""
import numpy as np
class PerformanceLogger:
    # average wait delay of the task as time series
    __averageWaitDelayOfTasks_timeSeries = [] #[ sec]
    # average wireless delay as time series
    __averageWirelessDelayOfTasks_timeSeries = []
    # average routing delay as time series
    __averageRoutingDelayOfTasks_timeSeries = []
    # average sending to cloud delay as time series
    __averageSendToCloudDelayOfTasks_timeSeries = []
    # average local execution as time series
    __averageExecDelayOfTasks_timeSeries = []
    __averageUserExecDelayOfTasks_timeSeries = []
    __SRT = 0 # system response time [sec]
    __RTR = 0 # refused tasks ratio
    __STR = 0 # served tasks ratio 
    __SRT_TS = [] # system response time as time series
    __RTR_TS = [] # refused tasks ratio as time series
    __STR_TS = [] # served tasks ratio as time series
    
    # for later use 
    __totalAverageWaitDelayOfTasks = 0 # [sec]
    __numberOfRefucedTasks = 0
    __numberOfServedTasks = 0
    __numberOfArrivedTasks = 0 
    __numberOfRefucedTasks_timeSeries = []
    __numberOfArrivedTasks_timeSeries = []
    __numberOfServedTasks_timeSeries = []
    __energyExec_TS = []
    __energySend_TS = []
    __totalEnergy_TS = []
    __userEnergyExec_TS = []
    __renting_TS = []
    # dictionaries with (timeCounter) keys
    __arrivedTasksNumberList = {}
    __rfusedTasksNumberList = {}
    __servedTasksNumberList = {}
    __wirelessDelayList = {}
    __delayOfRoutingList = {}
    __delayOfSendToCloudList = {}
    __waitDelayList ={}
    __timeExecList = {}
    __sendingEnergyList = {}
    __energyExecList = {}
    __userEnergyExecList = {}
    __delayOfUserExecList = {}
    __rentingList = {}
    #%% get functions
    def getAllMeasures(self):
        return self.__averageWirelessDelayOfTasks_timeSeries \
            , self.__averageRoutingDelayOfTasks_timeSeries \
            , self.__averageWaitDelayOfTasks_timeSeries \
            , self.__averageSendToCloudDelayOfTasks_timeSeries\
            , self.__averageExecDelayOfTasks_timeSeries
     
    def getSRT_TS(self):
        return self.__SRT_TS
    
    def getTotalEnerg_TS(self):
        return self.__totalEnergy_TS
    def getExecEnerg_TS(self):
        return self.__energyExec_TS
    
    def getSendingEnerg_TS(self):
        return self.__energySend_TS
    
    def getArrivedTasks_TS(self):
        return self.__numberOfArrivedTasks_timeSeries
    
     # get the served tasks ratio series
    def getSTR_TS(self):
        return self.__STR_TS
    
     # get the refuced tasks ratio time series 
    def getRTR_TS(self):
        return self.__RTR_TS
    # get userExec delay TS
    def getUserExecDelay_TS(self):
        return self.__averageUserExecDelayOfTasks_timeSeries
    # get userExec Energy
    def getUserExecEnergy_TS(self):
        return self.__userEnergyExec_TS
    # get renting
    def getRenting_TS(self):
        return self.__renting_TS
    #%% function calc_averageWaitDelayOfTasks_timeSeries
        # average of waiting delay 
    def calc_averageWaitDelayOfTasks_timeSeries(self,timeCounter):
        # find all wait delay tasks 
        if str(timeCounter)  in self.__waitDelayList.keys():
            self.__averageWaitDelayOfTasks_timeSeries.append\
                (np.mean(self.__waitDelayList[str(timeCounter)]))
        else:
            self.__averageWaitDelayOfTasks_timeSeries.append(0)
      #%% function    calc_averageWirelessDelayOfTasks_timeSeries        
    def calc_averageWirelessDelayOfTasks_timeSeries(self,timeCounter):
        # find all wait delay tasks 
        if str(timeCounter)  in self.__wirelessDelayList.keys():
            self.__averageWirelessDelayOfTasks_timeSeries.append\
                (np.mean(self.__wirelessDelayList[str(timeCounter)])) 
        else:
            self.__averageWirelessDelayOfTasks_timeSeries.append(0)
    #%% function calc_averageRoutingDelayOfTasks_timeSeries
    def calc_averageRoutingDelayOfTasks_timeSeries(self,timeCounter):
        # find all wait delay tasks 
        if str(timeCounter)  in self.__delayOfRoutingList.keys():
            self.__averageRoutingDelayOfTasks_timeSeries.append\
                (np.mean(self.__delayOfRoutingList[str(timeCounter)])) 
        else:
            self.__averageRoutingDelayOfTasks_timeSeries.append(0)
      #%%   function calc_averageSendToCloudDelayOfTasks_timeSeries       
    def calc_averageSendToCloudDelayOfTasks_timeSeries(self,timeCounter):
        # find all wait delay tasks 
        if str(timeCounter)  in self.__delayOfSendToCloudList.keys():
            self.__averageSendToCloudDelayOfTasks_timeSeries.append\
                (np.mean(self.__delayOfSendToCloudList[str(timeCounter)]))
        else:
            self.__averageSendToCloudDelayOfTasks_timeSeries.append(0)
    #%% function calc_averageExecDelayOfTasks_timeSeries
    def calc_averageExecDelayOfTasks_timeSeries(self,timeCounter):
        # find all wait delay tasks 
        if str(timeCounter)  in self.__timeExecList.keys():
            self.__averageExecDelayOfTasks_timeSeries.append\
                (np.mean(self.__timeExecList[str(timeCounter)])) 
        # 
        else:
            self.__averageExecDelayOfTasks_timeSeries.append(0)
    #%% function calc_averageUsersExecDelayOfTasks_timeSeries
    def calc_averageUsersExecDelayOfTasks_timeSeries(self,timeCounter):
        # find all wait delay tasks 
        if str(timeCounter)  in self.__delayOfUserExecList.keys():
            self.__averageUserExecDelayOfTasks_timeSeries.append\
                (np.mean(self.__delayOfUserExecList[str(timeCounter)])) 
        # 
        else:
            self.__averageUserExecDelayOfTasks_timeSeries.append(0)
    #%% function calc_totalAverageWaitDelayOfTasks
    def calc_totalAverageWaitDelayOfTasks(self):
        self.__totalAverageWaitDelayOfTasks = np.mean\
            (self.__averageWaitDelayOfTasks_timeSeries)

      #%%  function pickRefucedTasks
        # pick refuced tasks
    def pickRefucedTasks(self,timeCounter):
        self.__numberOfRefucedTasks +=1
        if str(timeCounter) not in self.__rfusedTasksNumberList.keys():
            self.__rfusedTasksNumberList[str(timeCounter)] =[]
            self.__rfusedTasksNumberList[str(timeCounter)].append(1)
        else:
            self.__rfusedTasksNumberList[str(timeCounter)].append(1)
        #%% function pickServedTasks
        # pick served tasks
    def pickServedTasks(self,timeCounter):
        self.__numberOfServedTasks +=1
        if str(timeCounter) not in self.__servedTasksNumberList.keys():
            self.__servedTasksNumberList[str(timeCounter)] = []
            self.__servedTasksNumberList[str(timeCounter)].append(1)
        else:
            self.__servedTasksNumberList[str(timeCounter)].append(1)
        #%% function pickArrivedTask
        # pick arrived tasks
    def pickArrivedTask(self,timeCounter):
        self.__numberOfArrivedTasks +=1
        if str(timeCounter) not in self.__arrivedTasksNumberList.keys():
            self.__arrivedTasksNumberList[str(timeCounter)] = []
            self.__arrivedTasksNumberList[str(timeCounter)].append(1)
        else:
            self.__arrivedTasksNumberList[str(timeCounter)].append(1)
    #%% function findArrivedTask_TS
    def findArrivedTask_TS(self,timeCounter):
        if str(timeCounter) in self.__arrivedTasksNumberList.keys():
            art = np.sum(self.__arrivedTasksNumberList[str(timeCounter)])
            self.__numberOfArrivedTasks_timeSeries.append(art)
        else:
            self.__numberOfArrivedTasks_timeSeries.append(0)
            #%% function findSRT_TS
    def findSRT_TS(self,timeCounter):
        srt = self.__averageWaitDelayOfTasks_timeSeries[timeCounter] + \
            self.__averageWirelessDelayOfTasks_timeSeries[timeCounter] + \
            self.__averageRoutingDelayOfTasks_timeSeries[timeCounter] + \
            self.__averageSendToCloudDelayOfTasks_timeSeries[timeCounter] + \
            self.__averageExecDelayOfTasks_timeSeries[timeCounter] + \
            self.__averageUserExecDelayOfTasks_timeSeries[timeCounter]
        # print("wait: ",self.__averageWaitDelayOfTasks_timeSeries[timeCounter] )
        # print("wireless: ",self.__averageWirelessDelayOfTasks_timeSeries[timeCounter] )
        # print("routing: ",self.__averageRoutingDelayOfTasks_timeSeries[timeCounter] )
        # print("cloud: ",self.__averageSendToCloudDelayOfTasks_timeSeries[timeCounter] )
        # print("exec: ", self.__averageExecDelayOfTasks_timeSeries[timeCounter] )
        # print("user exec: ",self.__averageUserExecDelayOfTasks_timeSeries[timeCounter] )
        self.__SRT_TS.append(srt)
    
    
     #%% function findExecEnergy_TS
    def findExecEnergy_TS(self,timeCounter):
       if str(timeCounter) in self.__energyExecList.keys():
            ee = np.sum(self.__energyExecList[str(timeCounter)])    
            self.__energyExec_TS.append(ee)
       else:
            self.__energyExec_TS.append(0)
     #%% function findSendEnergy_TS
    def findSendEnergy_TS(self,timeCounter):
       if str(timeCounter) in self.__sendingEnergyList.keys():
            se = np.sum(self.__sendingEnergyList[str(timeCounter)])    
            self.__energySend_TS.append(se)
       else:
            self.__energySend_TS.append(0)
    #%% function findSendEnergy_TS
    def findUserExecEnergy_TS(self,timeCounter):
       if str(timeCounter) in self.__userEnergyExecList.keys():
            se = np.sum(self.__userEnergyExecList[str(timeCounter)])    
            self.__userEnergyExec_TS.append(se)
       else:
            self.__userEnergyExec_TS.append(0)
        #%% function findRenting_TS
    def findRenting_TS(self,timeCounter):
       if str(timeCounter) in self.__rentingList.keys():
            rt = np.sum(self.__rentingList[str(timeCounter)])    
            self.__renting_TS.append(rt)
       else:
            self.__renting_TS.append(0)
            
     #%% function total energy
    def findTotalEnergy_TS(self,timeCounter):
       self.__totalEnergy_TS.append(self.__energySend_TS[timeCounter]+\
                                        self.__userEnergyExec_TS[timeCounter])
    
    #%% function findSTR_TS
        # find served tasks ratio time series
    def findSTR_TS(self,timeCounter):
        if str(timeCounter) in self.__servedTasksNumberList.keys()\
            and str(timeCounter) in self.__arrivedTasksNumberList.keys():
            STR = np.sum(self.__servedTasksNumberList[str(timeCounter)])/\
                np.sum(self.__arrivedTasksNumberList[str(timeCounter)])
            self.__STR_TS.append(STR)
        else:
            self.__STR_TS.append(0)
   
    #%% function findRTR_TS
    # refuced tasks ratio time series
    def findRTR_TS(self,timeCounter):
        if str(timeCounter) in self.__rfusedTasksNumberList.keys()\
            and str(timeCounter) in self.__arrivedTasksNumberList.keys():
            RTR = np.sum(self.__rfusedTasksNumberList[str(timeCounter)])/\
                np.sum(self.__arrivedTasksNumberList[str(timeCounter)])
            self.__RTR_TS.append(RTR)
        else:
            self.__RTR_TS.append(0)
   
    
    #%% function pickWirelessDelay
    def pickWirelessDelay(self,timeCounter,wi):
        if str(timeCounter) not in self.__wirelessDelayList.keys():
            self.__wirelessDelayList[str(timeCounter)] = []
            self.__wirelessDelayList[str(timeCounter)].append(wi)
        else:
            self.__wirelessDelayList[str(timeCounter)].append(wi)
     #%% function pickSendingEnergy
    def pickSendingEnergy(self,timeCounter,se):
        if str(timeCounter) not in self.__sendingEnergyList.keys():
            self.__sendingEnergyList[str(timeCounter)] = []
            self.__sendingEnergyList[str(timeCounter)].append(se)
        else:
            self.__sendingEnergyList[str(timeCounter)].append(se)
    # %% function pickDelayOfRouting
    def pickDelayOfRouting(self,timeCounter,delay):
        if str(timeCounter) not in  self.__delayOfRoutingList.keys():
             self.__delayOfRoutingList[str(timeCounter)] = []
             self.__delayOfRoutingList[str(timeCounter)].append(delay)
            
        else:
             self.__delayOfRoutingList[str(timeCounter)].append(delay)
    
    #%% function pickExecTime
    #execution time on server
    def pickExecTime(self,timeCounter,execTime):
        if str(timeCounter) not in  self.__timeExecList.keys():
            self.__timeExecList[str(timeCounter)] = []
            self.__timeExecList[str(timeCounter)].append(execTime)
        else:
            self.__timeExecList[str(timeCounter)].append(execTime)
    #%% function pickExecTime
    #execution time on server
    def pickExecEnergy(self,timeCounter,execEnergy):
        if str(timeCounter) not in  self.__energyExecList.keys():
            self.__energyExecList[str(timeCounter)] = []
            self.__energyExecList[str(timeCounter)].append(execEnergy)
        else:
            self.__energyExecList[str(timeCounter)].append(execEnergy)
    #%% function pickExecTimeUsers
    #execution time on server
    def pickUserExecEnergy(self,timeCounter,execEnergy):
        if str(timeCounter) not in  self.__energyExecList.keys():
            self.__userEnergyExecList[str(timeCounter)] = []
            self.__userEnergyExecList[str(timeCounter)].append(execEnergy)
        else:
            self.__userEnergyExecList[str(timeCounter)].append(execEnergy)
    #%% function pickDelayOfSendToCloud
    def pickDelayOfSendToCloud(self,timeCounter,delay):
        if str(timeCounter) not in  self.__delayOfSendToCloudList.keys():
            self.__delayOfSendToCloudList[str(timeCounter)] = []
            self.__delayOfSendToCloudList[str(timeCounter)].append(delay)
        else:
            self.__delayOfSendToCloudList[str(timeCounter)].append(delay)
    #%% function pickDelayOfUserExec
    def pickDelayOfUserExec(self,timeCounter,delay):
        if str(timeCounter) not in  self.__delayOfUserExecList.keys():
            self.__delayOfUserExecList[str(timeCounter)] = []
            self.__delayOfUserExecList[str(timeCounter)].append(delay)
        else:
            self.__delayOfUserExecList[str(timeCounter)].append(delay)
    #%% function pickWaitDelayOfTask
    def pickWaitDelayOfTask(self,timeCounter,delay):
        if str(timeCounter) not in  self.__waitDelayList.keys():
             self.__waitDelayList[str(timeCounter)] = []
             self.__waitDelayList[str(timeCounter)].append(delay)
        else:
             self.__waitDelayList[str(timeCounter)].append(delay)
             
     #%% function pickWaitDelayOfTask
    def pickRenting(self,timeCounter,renting):
        if str(timeCounter) not in  self.__rentingList.keys():
             self.__rentingList[str(timeCounter)] = []
             self.__rentingList[str(timeCounter)].append(renting)
        else:
             self.__rentingList[str(timeCounter)].append(renting)
#%% end  