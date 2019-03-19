# TODO: Add multiprocessing functionality

import numpy as np
from numba import jit, njit
from itertools import permutations, islice

def validate(pieces):
    """Validate if pieces are assembled in a valid configuration.
    
    Parameters
    ----------
    pieces : array like
        an array with 19 numbers, each number being 
        a number between 1 and 19, and allowing no 
        number to repeat.
    
    Returns
    -------
    result : Boolean
        Returns True if solution is valid, otherwise returns False.
    """ 

    ans = np.array(pieces)
    # check if pieces is a valid input
    if not np.array_equal(sorted(ans), np.arange(1,20)):
        raise ValueError("""Pieces must be any ordering of the array
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]""")
   
    # create board configurations
    configs = [ans, rotate_pieces(ans)]
    configs.append(rotate_pieces(configs[1]))

    # check sums
    result = np.all(np.array([np.all(check_rows(config)) for config in np.array(configs)]))  
    return result

def brute_force(start=0, stop=None, logThreshold=10000):
    """Solve puzzle via brute force.
    
    Parameters
    ----------
    start : int (default = 0)
        The iteration the permutation generator should start at.

    stop : int (default = None)
        The iteration the permutation generator should stop at. 
        None tells the generator to run until completion.

    logThreshold : int (default = 10000)
        The amount of iterations prior to printing a status report.
    
    Returns
    -------
    None        
    """ 
    
    cnt = start
    perms = permutations(list(range(1,20)), 19)
    if start != 0:
        perms = islice(perms, start, stop)
    
    try:
        while True:
            current = perms.__next__()
            cnt += 1
            if cnt % logThreshold == 0:
                print('Now on iteration ', cnt)
                print('Now attempting solution: ', current)
            if validate(current):
                return cnt, current
    except StopIteration:
        return None
    except KeyboardInterrupt:
        print(cnt)

@jit
def rotate_pieces(ans):
    """Rotates the puzzle board.
    
    Parameters
    ----------
    ans : array like
        an array with 19 numbers, each number being 
        a number between 1 and 19, and allowing no 
        number to repeat.
    
    Returns
    -------
    : np.array
        Returns ans rearranged to reflect board rotation.
    """ 
    return np.array([
        ans[2], ans[6], ans[11],
        ans[1], ans[5], ans[10], ans[15],
        ans[0], ans[4], ans[9],  ans[14], ans[18],
        ans[3], ans[8], ans[13], ans[17], 
        ans[7], ans[12],ans[16]
    ])

@njit
def check_rows(ans):
    """Checks whether sums of each horizontal row is 38
    
    Parameters
    ----------
    ans : array like
        an array with 19 numbers, each number being 
        a number between 1 and 19, and allowing no 
        number to repeat.
    
    Returns
    -------
    : Boolean
        Returns a boolean, signifying whether all 5 rows each 
        sum up to 38.
    """ 
    checks = np.array([
        np.sum(ans[:3]) == 38, 
        np.sum(ans[3:7]) == 38,
        np.sum(ans[7:12]) == 38,
        np.sum(ans[12:16]) == 38,
        np.sum(ans[16:]) == 38,
    ])

    return np.all(checks)

if __name__ == "__main__":
    start = int(input('Start Iteration: '))
    while True:
        iteration, solution = brute_force(start=start, logThreshold=500000)
        print('Solution for iteration ', iteration, ':\n', solution)
        input('Press ENTER to continue.')
        start = iteration
