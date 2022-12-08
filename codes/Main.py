# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 10:38:11 2021

@author: Eng.Mohammad Sakka
"""
import matplotlib.pyplot as plt
import numpy as np
import WMAN
import Visualizer
import convertTimeUnit
from threading import Thread
#from inputNumpyArray import inputNumpyArray
#%% initialization
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
    get_ipython().magic('reset -f')
except:
    pass
#%% input parameters
deltaT = 30 # for optimization triggering
areaDims = (100*1000,100*1000) # Metropolitan area dimensions in meters
BSsNum = 50 # number of base station
initialUserRange = (1,100) # range of initial users in the system
cloudletsNum = 6 # number of cloudlets ,Note: the cloudlets are generated randomly,\
    # , so this number is not necessarily the same as that will be 
numberOfServersPerCloudlet = 5 # number of servers per the cloudlet
BScommDataRate = 3*10**8 # base station communication datarate [bit/sec]
wirelessDataRate = 2**10 # [bit/sec]
B = 50*(2**20) # internet connection data rate [bit/sec]
wirelessDelayPerMeter = 1 # wireless delay between base station and user per meter [10ms/m]
dataPucketSize = 8*1024 # 1 KB
lamdaMax = 45 # maximum workload accepted in the cloudlet
simulationPeriod = 1* 60 # simulation period in [second]
timeUnit = 1 # [system is updated each timeUnit [sec]]
#%% cost function parameters
zeta = 5 * 10**-27
phi_u = 2 * 2**30
phi_c = 8 * 2**30
phi_s = 4 * 2**30
p = 0.1
w = 40 * 2*20
lamdaMax = lamdaMax
B = B
numberOfServers = numberOfServersPerCloudlet
rentingRate = 10
#%% set the random generator seed
seed = 1
np.random.seed(seed)
#%% create WMAN object
wman = WMAN.WMAN(areaDims,BSsNum,initialUserRange,cloudletsNum,numberOfServersPerCloudlet\
                 ,BScommDataRate,wirelessDelayPerMeter,wirelessDataRate,dataPucketSize,lamdaMax,B,\
                     deltaT)

# %% create the visualizer object
visualizer = Visualizer.Visualizer()
hl = visualizer.visSystem(wman)
#%% running the system
simulationPeriodInMs = convertTimeUnit.convertSecToTimeUnit(timeUnit, simulationPeriod)
# new_thread = Thread(visualizer.updateVisualization)
# new_thread.start()
for timeCounter in range(int(simulationPeriodInMs)):
    isZset = True
    #%% # to do by Hussam
     #if timeCounter%deltaT == 0 and timeCounter!=0:
        # initial_Z = wman.getZ()
        # initial_X = wman.getX()
       #  users =  wman.getUsers()
    #     Z,X = optimizer() 
    #     input("wait for optimizer decision")
      #   wman.set_Z(Z)
       #  wman.set_X(X)
        #%%
    
    wman.DoingMyRoutine(timeCounter, isZset)
    # if not visualizer.closed:

visualizer.updateVisualization(wman, hl)
# plt.show()


    

