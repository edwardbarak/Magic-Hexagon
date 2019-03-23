from itertools import permutations
from numba import njit
import numpy as np

def main():
    allPieces = np.arange(1,20)
    
    # all possible permutations for row 1
    perms = np.array(list(permutations(allPieces, 3)))
    
    # all possible permutations for row 1 where the sum is 38
    perms = [np.array(perm, dtype=np.int8) for perm in perms if np.array(perm, dtype=np.int8).sum() == 38]
    
    # append all possible row 5 permutations whose sum is 38 to their respective row 1 permutations
    for i in range(len(perms)):
        _diff = np.setdiff1d(allPieces, np.array(perms[i], dtype=np.int8))
        _r5s = np.array([np.array(perm, dtype=np.int8) for perm in permutations(_diff, 3) if np.array(perm, dtype=np.int8).sum() == 38])
        perms[i] = [perms[i], _r5s]

    # flatten perms so that each value in perms is an array of length 19, 
    # with positions that don't have pieces placed represented by zeros.
    _perms = []
    _zeros = np.zeros(13,dtype=np.int8)
    
    for i in range(len(perms)):
        for j in range(len(perms[i][1])):
            # _perms.append(list(perms[i][0]) + [0] * 13 + list(perms)[i][1][j])
            _perms.append(np.concatenate([perms[i][0], _zeros, perms[i][1][j]]))
    perms = _perms
    
    # convert perms so that all permutations using leftover pieces for 
    # positions 3, 7, & 12 sum up correctly to their respective permutations
    _perms = []
    _cntr = 0
    for perm in perms:        
        _diff = np.setdiff1d(allPieces, perm)
        for perm3712 in permutations(_diff, 3):
            _cntr += 1
            if _cntr % 10000 == 0: print(_cntr)

            pieces037 = np.sum(perm[0] + perm3712[0] + perm3712[1], dtype=np.int8)
            pieces71217 = np.sum(perm[17] + perm3712[2] + perm3712[1], dtype=np.int8)
            if pieces037 == pieces71217 == np.int8(38):
                _perm = perm[[3, 7, 12]] = np.array(perm3712, dtype=np.int8)
                _perms.append(_perm)
    perms = _perms

    return perms

def test3712(perms):
    allPieces = np.array(np.arange(1,20), dtype=np.int8)
    perms = np.array(perms, dtype=np.int8)
    _diff = np.setdiff1d(allPieces, perm)