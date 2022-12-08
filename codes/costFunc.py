# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 21:37:49 2021

@author: mhdsq
"""
import numpy as np
def optimizer_costFunc(X,Z,zeta,phi_u,phi_s,phi_c,p,users,w,lamdaMax,B,numberOfServers\
                       ,rentingRate):
    # X,Z: decision variables
    # zeta: effective switched capacitance of user's CPU [no unit]
    # phi_u: computing capacity of user [cycles/sec]
    # phi_s: computing capacity of server in cloudlet [cycles/sec]
    # phi_c: computing capacity of the cloud [cycles/sec]
    # p: transmission power of user [Watt]
    # users: system users
    # w: wireless data transmission rate [bit/sec]
    # lamdaMax: maximum number of tasks in cloudlet [task]
    # B: internet speed [bit/sec]
    # numberOfServers: number of servers per cloudlet (same for all cloudlets) [server]
    # rentingRate : renting rate of cloudlet server [$/sec]
    
    
    # objective 1: number of cloudlets
    cloudlets = np.array(np.nonzero(X==1))
    numberOfCloudlets = (cloudlets.shape[1])
    psi3 = numberOfCloudlets
    # objective 2: energy consumption
    avgCompDemandOfUsers = []
    avgTasksSizeOfUsers = []
    avgTaskArrivalRateOfUsers = []
    for u in users:
        avgCompDemandOfUsers.append(u.averageCompDemand)
        avgTasksSizeOfUsers.append(u.averageDataSize)
        avgTaskArrivalRateOfUsers.append(u.taskSendingRate)
    ec = zeta * (phi_u**2) * np.array(avgCompDemandOfUsers)
    et = (p * np.array(avgTasksSizeOfUsers)) / w
    e1 = ec * np.array(avgTaskArrivalRateOfUsers) * (1-Z.sum(axis=1))
    e2 = et * np.array(avgTaskArrivalRateOfUsers) * (Z.sum(axis=1))
    e = e1 + e2
    psi1 = e.mean()
    
    # objective3: time delay
    avgCompDemandOfUsers = np.array(avgCompDemandOfUsers)
    avgTasksSizeOfUsers = np.array(avgTasksSizeOfUsers)
    avgTaskArrivalRateOfUsers = np.array(avgTaskArrivalRateOfUsers)
    # the average waiting time composed of the
    # queue and execution time for executing a task of ui locally 
    den1 = avgCompDemandOfUsers * avgTaskArrivalRateOfUsers
    ones1 = np.ones(len(avgCompDemandOfUsers))
    den2 = ones1 - Z.sum(axis=1)
    den3 = den1 * den2
    den = phi_u*ones1 - den3
    Tl = avgCompDemandOfUsers/den
    
    # the average waiting time consisting of the queue and transmission
    # time for transmitting an offloaded task of ui to its
    # associated BS
 
    Tt = (avgTasksSizeOfUsers * avgTaskArrivalRateOfUsers * Z.sum(axis=1))/w
    
    numberOfSentToCloudTasks =  np.ceil(avgTaskArrivalRateOfUsers.conj().T\
                                        @ Z).sum() - lamdaMax*Z.shape[1]
    numberOfNotSentToCloudTasks = lamdaMax
    if numberOfSentToCloudTasks < 0:
        numberOfSentToCloudTasks = 0
    # the queue and execution time for executing
    # a task in a cloudlet ci is 
    if numberOfSentToCloudTasks > 0:
        Tc = (numberOfNotSentToCloudTasks * avgTasksSizeOfUsers.mean())/\
            (numberOfCloudlets * numberOfServers * phi_s)
        
    else:
        tmp =  avgTaskArrivalRateOfUsers * avgCompDemandOfUsers
        tmp = Z.conj().T @ tmp
        tmp2 = Z.conj().T @ avgTaskArrivalRateOfUsers
        num = tmp/tmp2
        den = phi_s*ones1*numberOfServers - tmp
        Tc = num/den
        Tc = Tc.mean()
    # the send to cloud delay
    TtCloud = (numberOfSentToCloudTasks * avgTasksSizeOfUsers.mean()) / B
    TeCloud = (numberOfSentToCloudTasks * avgCompDemandOfUsers.mean()) / phi_c
    Tcloud = TtCloud + TeCloud
    
    sumZalongCols = Z.sum(axis=1)
    term = ones1 - sumZalongCols
    term = term * Tl
    term2 = (Tcloud + Tc + Tt)* Z
    term2 = term2.sum(axis=1)
    
    T = term + term2
    T = T.mean()
    psi2 = T
    
    # renting Cost 
    renting = Tc * rentingRate
    psi4 = renting.mean()
    
    return psi1,psi2,psi3,psi4
    