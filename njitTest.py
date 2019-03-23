from numba import njit
from itertools import permutations
import numpy as np

def main():
    perms0 = np.array(list(permutations(np.arange(1,20),3)))
    row1 = is38(perms0, 3)
    
    perms1 = np.array()
    
@njit
def is38(perms, step):
    return np.array([perms[i] + perms[i+1] + perms[i+2] == 38] for i in np.arange(0,len(perms),step)])