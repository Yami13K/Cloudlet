# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 22:31:25 2021

@author: mhdsq
"""
import numpy as np
def inputNumpyArray():
    R = int(input("Enter the number of rows:"))
    C = int(input("Enter the number of columns:"))
    # Initialize matrix
    matrix = []
    print("Enter the entries rowwise:")
      
    # For user input
    for i in range(R):          # A for loop for row entries
        a =[]
        for j in range(C):      # A for loop for column entries
             a.append(int(input()))
        matrix.append(a)
      
    # For printing the matrix
    for i in range(R):
        for j in range(C):
            print(matrix[i][j], end = " ")
        print()
    matrix = np.array(matrix)
    return matrix