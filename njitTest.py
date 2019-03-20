from numba import njit
from itertools import permutations
import numpy as np

def row5(perms):
    row5s = np.array([row for row in perms])
    return row5s