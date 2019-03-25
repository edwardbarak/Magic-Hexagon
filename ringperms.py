#!/usr/bin/env python3

from itertools import permutations
from time import time
import numpy as np

elapsed = lambda start: print('\nTime: %s' % (time() - start))

def solve(runtime=False):
    if runtime: start = time()
    allPieces = np.arange(1,20, dtype=np.int8)
    
    try:    
        # OUTER RING CALCULATIONS

        # generate all possible permutations of pieces in pos 1,2,3
        perms = np.array(tuple(permutations(allPieces, 3)), dtype=np.int8)
        # only keep permutations where pieces in pos 1,2,3 sum up to 38
        perms = perms[np.where(np.sum(perms, axis=1) == 38)]        
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
        # append result of 38 - (pos1 + pos8) to every row
        # calculate what pos4 must be
        _pos4diffs = np.subtract(38, perms[:,[0,-1]].sum(axis=1)).astype(np.int8)
        # check if pos4 <= 19, since no piece larger than 19 exists
        _isBetween1and19 = _pos4diffs <= 19
        # all perms and pos4 where pos4 <= 19,
        _pos4diffs = _pos4diffs[np.where(_isBetween1and19)]
        perms = perms[np.where(_isBetween1and19)]
        perms = np.append(perms, _pos4diffs[:,None], axis=1)
        # all perms where the piece in pos4 hasn't already been used in a different pos
        _pos4notUsed = np.array([perm[-1] not in perm[:-1] for perm in perms])
        perms = perms[np.where(_pos4notUsed)]

        # INNER RING CALCULATIONS
        # solve for pos5, pos9
        # _perms for pos5, pos9
        # get leftover pieces for each sequence
        _diff_func = lambda x: np.setdiff1d(allPieces, x)
        _diff = np.apply_along_axis(_diff_func, 1, perms)
        # get permutations of leftover pieces
        _getNewPerms = lambda x: np.array(tuple(permutations(x, 2)), dtype=np.int8)
        _newperms = np.apply_along_axis(_getNewPerms, 1, _diff)
        # append _newperms to perms
        perms = np.repeat(perms, _newperms.shape[1], axis=0)
        _newperms = _newperms.reshape(np.prod(_newperms.shape[:2]), _newperms.shape[2])
        perms = np.append(perms, _newperms, axis=1)
        # keep all perms where 38 - sum(pos2,pos13) == pos5 + pos9
        # pos2 = perm[1], pos13 = perm[9] 
        perms = perms[np.where(38 - perms[:,[1, 9]].sum(axis=1) == perms[:,-2:].sum(axis=1))]        
        # get pos6
        # where 38 - sum(pos4, pos5, pos7) in setdiff(allPieces) 
        # pos4 = perm[11], pos5 = perm[13], pos7 = perm[3]
        perms = np.append(perms, (38 - perms[:,[11,13,3]].sum(axis=1))[:,None], axis=1)
        perms = perms[np.where(np.array([np.unique(perm).shape == perm.shape for perm in perms], dtype=np.int8))]
        # get pos11 at perm[15]. use pos2 @ perm[1], pos6 @ perm[14], and pos16 @ perm[5]
        perms = np.append(perms, (38 - perms[:,[1,14,5]].sum(axis=1))[:,None], axis=1)
        perms = perms[np.where(np.array([np.unique(perm).shape == perm.shape for perm in perms], dtype=np.int8))]
        # get pos15 at perm[16]. use pos7 @ perm[3], pos18 @ perm[7], and pos11 @ perm[15]
        perms = np.append(perms, (38 - perms[:,[3,7,15]].sum(axis=1))[:,None], axis=1)
        perms = perms[np.where(np.array([np.unique(perm).shape == perm.shape for perm in perms], dtype=np.int8))]
        # get pos14 at perm[17]. use pos16 @ perm[5], pos15 @ perm[16], and pos13 @ perm[9]
        perms = np.append(perms, (38 - perms[:,[5,16,9]].sum(axis=1))[:,None], axis=1)
        perms = perms[np.where(np.array([np.unique(perm).shape == perm.shape for perm in perms], dtype=np.int8))]

    except KeyboardInterrupt:
        pass

    if runtime: elapsed(start)
    return perms