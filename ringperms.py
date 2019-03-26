#!/usr/bin/env python3

from itertools import permutations
from time import time
import numpy as np

elapsed = lambda start: print('\nTime: %s' % (time() - start))

def solve(runtime=True):
    # Initializations
    if runtime: start = time()    
    
    # Settings
    allPieces = np.arange(1,20, dtype=np.int8)

    try:    
        # OUTER RING CALCULATIONS
        # Generate all possible choices for positions 1, 2, & 3
        _newperms = permutations(allPieces, 3)
        perms = np.array(tuple(_newperms), dtype=np.int8)
        # Filter out choices where where pieces in positions 1, 2, & 3 do not sum up to 38
        perms = perms[np.where(np.sum(perms, axis=1) == 38)]        
        
        # Find the remaining pieces for the outer ring
        for i in range(4):
            # Find possible choices for the next 2 pieces
            _newperms = np.array([tuple(permutations(np.setdiff1d(allPieces, perm), 2)) for perm in perms], dtype=np.int8)
            perms = np.array([np.repeat([perm], _newperms.shape[1], axis=0) for perm in perms]) # Transform
            perms = np.append(perms, _newperms, axis=2)                                         # Transform
            perms = perms.reshape(np.prod(perms.shape[:2]), perms.shape[2])                     # Transform
            perms = perms[np.where(perms[:,-3:].sum(axis=1) == 38)]                             # Filter
            
        # Find the final piece of the outer ring
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
        
        # Solve for positions 6, 11, 14, & 15
        placeDifference = lambda perms, x, y, z: np.append(perms, (38 - perms[:,[x,y,z]].sum(axis=1))[:,None], axis=1)
        placeDifferenceValidation = lambda perms: perms[np.where(np.array([np.unique(perm).shape == perm.shape for perm in perms], dtype=np.int8))]
                
        dependents = [
            [11,13,3], # position  6 dependents
            [1,14,5],  # position 11 dependents
            [3,7,15],  # position 14 dependents
            [5,16,9],  # position 15 dependents
            ]
        
        for i in dependents:
            perms = placeDifference(perms, i[0], i[1], i[2])
            perms = placeDifferenceValidation(perms)

        # Solve for position 10
        perms = np.append(perms, np.array([np.setdiff1d(allPieces, perm)[0] for perm in perms], dtype=np.int8)[:,None], axis=1)
        results = perms[np.nonzero(test(perms, False, False))]
        
    except KeyboardInterrupt:
        if runtime: elapsed(start)        
        return None

    if runtime: elapsed(start)
    return reorganize(results)

def test(solutions, runtime=True, report=True):
    if runtime: start = time()

    results = np.array([38 
    # test 3s
    == s[:3].sum() 
    == s[2:5].sum() 
    == s[4:7].sum()
    == s[6:9].sum()
    == s[8:11].sum()
    == s[[0,10,11]].sum()
    # test 4s
    == s[[1,13,12,9]].sum()
    == s[[9,17,16,5]].sum()
    == s[[5,15,14,1]].sum()
    == s[[11,12,17,7]].sum()
    == s[[7,16,15,3]].sum()
    == s[[3,14,13,11]].sum()
    # test 5s
    == s[[10,12,18,15,4]].sum()
    == s[[0,13,18,16,6]].sum()
    == s[[2,14,18,17,8]].sum()
    for s in solutions]).astype(np.int8)

    if runtime: elapsed(start)
    if report: 
        correct = results.sum()
        incorrect = results.shape[0] - correct
        score = float(correct) / results.shape[0]
        print('Correct solutions: {}\nIncorrect Solutions: {}\nScore: {}'.format(correct, incorrect, score))

    return results

def reorganize(solutions, order=[0,1,2,11,13,14,3,10,12,18,15,4,9,17,16,5,8,7,6]):    
    return np.array([solution[order] for solution in solutions], dtype=np.int8)