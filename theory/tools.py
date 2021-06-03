import numpy as np

def compute_degrees(mat):
    no_weight_mat = mat.copy()
    no_weight_mat[no_weight_mat>0] = 1
    
    sum_col = np.sum(no_weight_mat, axis=0)
    sum_line = np.sum(no_weight_mat, axis=1)
    
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

def mat_to_edges(n, mat):
    edge =  []
    for i in range(n):
        for j in range(n):
            if (mat[i][j]):
                edge.append((i,j,mat[i][j]))
    return edge