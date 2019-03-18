import numpy as np
from numba import njit
from itertools import permutations

@njit
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
    if sorted(ans) != np.arange(1,20):
        raise ValueError('Pieces must be any ordering of output: list(range(1,20))')
       
    # rules
    pass

def brute_force():
    """Solve puzzle via brute force."""
    pass