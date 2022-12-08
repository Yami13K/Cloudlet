# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 15:03:27 2021

@author: mhdsq
"""
#%% random walk demo [1-D]
import numpy as np
import matplotlib.pyplot as plt
x = [0]
t=[0]
f = plt.figure()
for t1 in range(100):
    x1 = x[t1] + np.random.normal(0,0.5)
    x.append(x1)
   
    t.append(t1)
plt.figure(f.number)
plt.plot(t,x,'*b:')
plt.show()  
    
    
    