# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 18:40:03 2022

@author: mhdsq
"""
from costFunc import optimizer_costFunc
import numpy as np
import User
X = np.array([0,0,1,0,0,1,0,0,1,0])
Z = np.array([[0.1,0.0,0.4],[0.0,0.4,0.05],[0.2,0.3,0.01]])
zeta = 5 * 10**-27
phi_u = 2 * 2**30 # computing capacity for user cpu
phi_c = 8 * 2**30 # computing capacity for  cloud
phi_s = 4 * 2**30# computing capacity for cloudlet server
p = 0.1 # user tranmission power
users = []
for i_usr in range(3):
    u = User.User([10,10],1)
    users.append(u)
w = 40 * 2*20 # wirless data rate
lamdaMax = 100 # maximum workload of cloudlet
B = 50 * 2**20 # internet speed
numberOfServers = 2 # per cloudlet
rentingRate = 10 # [$/sec] for server
# p1: cloudlets number
# p2: time delay
# p3: energy consumption
# p4: renting
p1,p2,p3,p4 = optimizer_costFunc(X,Z,zeta,phi_u,phi_s,phi_c,p,users,w,lamdaMax,B,numberOfServers\
                       ,rentingRate)