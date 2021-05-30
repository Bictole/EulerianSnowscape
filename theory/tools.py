# -*- coding: utf-8 -*-
"""
Created on Sun May 30 15:06:19 2021

@author: morin
"""

import numpy as np

def compute_degrees(mat):
    no_weight_mat = np.matrix(mat)
    no_weight_mat[no_weight_mat>0] = 1
    
    sum_col = np.sum(no_weight_mat, axis=0).flatten().tolist()[0]
    sum_line = np.sum(no_weight_mat, axis=1).flatten().tolist()[0]
    
    return (sum_line,sum_col)

def compute_charge(sum_line, sum_col, n):
    souscharge = []
    surcharge = []

    for i in range(n):
        if (sum_col[i] > sum_line[i]):
            souscharge.append(i)
                
        elif (sum_line[i] > sum_col[i]):
            surcharge.append(i)
            
    return (surcharge,souscharge)

        