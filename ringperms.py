#!/usr/bin/env python3

# from numba import njit
from itertools import permutations
from time import time
import numpy as np

elapsed = lambda start: print('\nTime: %s' % (time() - start))

def testing(runtime=False):
    if runtime: start = time()
    allPieces = set(range(1,20))

    try:    
        # generate all possible permutations of pieces in pos 1,2,3
        perms = np.array(tuple(permutations(allPieces, 3)), dtype=np.int8)
        # generate all possible permutations of pieces in pos 1,2,3 where the sum of those pieces is 38
        perms = perms[np.where(np.sum(perms, axis=1) == 38)]
        # all possible permutations of pos 7, 12, appended to respective permutation sequence
        perms = [[(np.append(perm, np.array(perm2, dtype=np.int8))) for perm2 in permutations(allPieces.difference(perm),2)] for perm in perms]
        perms = np.array(perms)
        # reshape 3d array to 2d, so each row is a valid permutation sequence
        perms = perms.reshape(perms.shape[0] * perms.shape[1], perms.shape[2])
        # all possible permutations of pos 7, 12 where the sum of pos 3, 7, & 12 is 38
        perms = perms[np.where(perms[:,2:].sum(axis=1) == 38)]
        return perms
    except KeyboardInterrupt:
        pass

    if runtime: print('\nTime: %s' % (time() - start))

def solve(runtime=False):
    if runtime: start = time()
    allPieces = np.arange(1,20, dtype=np.int8)
    
    try:    
        # generate all possible permutations of pieces in pos 1,2,3
        perms = np.array(tuple(permutations(allPieces, 3)), dtype=np.int8)
        # only keep permutations where pieces in pos 1,2,3 sum up to 38
        perms = perms[np.where(np.sum(perms, axis=1) == 38)]
        print(perms.shape)
        # find valid pieces for the following positions, two at a time, in sequential order: ((7,12), (16,19), (18,17), (13,8))
        for i in range(4):
            # get all possible permutations for next 2 positions, appeneded to their respective sequences
            # get all possible permutations of perms for one of the pairs of positions mentioned above
            _newperms = np.array([tuple(permutations(np.setdiff1d(allPieces, perm), 2)) for perm in perms], dtype=np.int8)
            # merge perms with their new respective permutations
            perms = np.array([np.repeat([perm], _newperms.shape[1], axis=0) for perm in perms])
            perms = np.append(perms, _newperms, axis=2)
            perms = perms.reshape(np.prod(perms.shape[:2]), perms.shape[2])
            # only keep permutations where the last 3 calculated pieces sum up to 38
            perms = perms[np.where(perms[:,-3:].sum(axis=1) == 38)]
            
        # find piece for position 4
        # TODO: if 38 - perm[[0,-1]].sum() in setdiff then add perm to perms

        
    except KeyboardInterrupt:
        pass

    if runtime: elapsed(start)
    return perms