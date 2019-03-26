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
        _newperms = permutations(allPieces, 3)                                                  # Generation
        perms = np.array(tuple(_newperms), dtype=np.int8)
        # Filter out choices where where pieces in positions 1, 2, & 3 do not sum up to 38
        perms = perms[np.where(np.sum(perms, axis=1) == 38)]                                    # Filtration        
        
        # Find the remaining pieces for the outer ring
        for i in range(4):
            # Find possible choices for next 2 pieces in the outer ring
            _newperms = np.array([tuple(permutations(np.setdiff1d(allPieces, perm), 2)) for perm in perms], dtype=np.int8)
            perms = np.array([np.repeat([perm], _newperms.shape[1], axis=0) for perm in perms]) # Transformation
            perms = np.append(perms, _newperms, axis=2)                                         # Transformation
            perms = perms.reshape(np.prod(perms.shape[:2]), perms.shape[2])                     # Transformation
            perms = perms[np.where(perms[:,-3:].sum(axis=1) == 38)]                             # Filtration
            
        # Find the final piece of the outer ring
        _differences = np.subtract(38, perms[:,[0,-1]].sum(axis=1)).astype(np.int8)             # Subtraction
        _isValidPiece = _differences <= 19                                                      # Validation
        _differences = _differences[np.where(_isValidPiece)]                                    # Filtration        
        perms = perms[np.where(_isValidPiece)]                                                  # Filtration

        perms = np.append(perms, _differences[:,None], axis=1)                                  # Transformation
        _isValidPiece = np.array([perm[-1] not in perm[:-1] for perm in perms])                 # Transformation
        perms = perms[np.where(_isValidPiece)]                                                  # Filtration

        # INNER RING CALCULATIONS
        # Find the first two pieces of the inner ring
        _get_difference = lambda x: np.setdiff1d(allPieces, x)
        _differences = np.apply_along_axis(_get_difference, 1, perms)                           # Subtraction
        
        _getNewPerms = lambda x: np.array(tuple(permutations(x, 2)), dtype=np.int8)
        _newperms = np.apply_along_axis(_getNewPerms, 1, _differences)                          # Generation
        
        perms = np.repeat(perms, _newperms.shape[1], axis=0)                                    # Transformation
        _newperms = _newperms.reshape(np.prod(_newperms.shape[:2]), _newperms.shape[2])         # Transformation
        perms = np.append(perms, _newperms, axis=1)                                             # Transformation

        perms = perms[np.where(38 - perms[:,[1, 9]].sum(axis=1) == perms[:,-2:].sum(axis=1))]   # Filtration        
        
        # Find the remaining pieces of the outer ring
        placeDifference = lambda perms, x, y, z: np.append(perms, (38 - perms[:,[x,y,z]].sum(axis=1))[:,None], axis=1)
        placeDifferenceValidation = lambda perms: perms[np.where(np.array([np.unique(perm).shape == perm.shape for perm in perms], dtype=np.int8))]
                
        dependents = [
            [11,13,3], # position  6 dependents
            [1,14,5],  # position 11 dependents
            [3,7,15],  # position 14 dependents
            [5,16,9],  # position 15 dependents
            ]
        
        for i in dependents:
            perms = placeDifference(perms, i[0], i[1], i[2])                                    # Subtraction
            perms = placeDifferenceValidation(perms)                                            # Validation

        # Find the centeral piece (last piece)
        _differences = [np.setdiff1d(allPieces, perm)[0] for perm in perms]                     # Subtraction
        perms = np.append(perms, np.array(_differences, dtype=np.int8)[:,None], axis=1)         # Transformation
        results = perms[np.nonzero(test(perms, False, False))]                                  # Filtration
        
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