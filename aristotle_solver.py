from numba import jit, njit
from itertools import permutations
import numpy as np

@jit
def solve():
    pieces = np.arange(1,20)
    # for each row5 in permutations(np.arange(1,20), 3) where np.sum(row5) == 38:
    for row5 in permutations(pieces, 3):
        if np.sum(row5) == 38:
            # lessRow5 = np.setdiff1d(np.arange(1,20), row5)
            lessRow5 = np.setdiff1d(pieces, row5)
            # for each row4 in permutations(lessRow5, 4) where np.sum(row4) == 38:
            for row4 in permutations(lessRow5, 4):
                if np.sum(row4) == 38:
                    # lessRow4 = np.setdiff1d(lessRow5, row4)
                    lessRow4 = np.setdiff1d(lessRow5, row4)
                    print('lessRow4: ', lessRow4)
                    # for each row3 in permutations(lessRow4, 5) where np.sum(row3) == 38:
                    for row3 in permutations(lessRow4, 5):
                        sol81317 = np.sum([row3[0], row4[0],row5[0]])
                        sol121619 = np.sum([row3[-1], row4[-1],row5[-1]])
                        if np.sum(row3) == sol81317 == sol121619 == 38:
                            # lessRow3 = np.setdiff1d(lessRow4, row3)
                            lessRow3 = np.setdiff1d(lessRow4, row3)
                            print('lessRow3: ', lessRow3)
                            # for each row2 in permutations(lessRow3, 4) where np.sum(row3) == 38:
                            for row2 in permutations(lessRow3, 4):
                                sol491418 = np.sum([row2[0], row3[1], row4[1], row5[1]])
                                sol7111518 = np.sum([row2[-1], row3[-2], row4[-2], row5[-2]])
                                if np.sum(row2) == sol491418 == sol7111518 == 38:
                                    lessRow2 = np.setdiff1d(lessRow3, 3)
                                    print('lessRow2: ', lessRow2)
                                    for row1 in permutations(lessRow2,3):
                                        sol148 = np.array([row1[0], row2[0], row3[0]])
                                        sol3712 = np.array([row1[-1], row2[-1], row3[-1]])
                                        sol25913 = np.array([row1[1], row2[1], row3[1], row4[0]])
                                        sol261116 = np.array([row1[-2], row2[-2], row3[-2], row4[-1]])
                                        sol15101519 = np.array([row1[0], row2[1], row3[2], row4[2], row5[2]])
                                        sol36101417 = np.array([row1[-1], row2[-2], row3[2], row4[1], row5[0]])
                                        if np.sum(row1) == np.sum(sol148) == np.sum(sol3712) == np.sum(sol25913) == np.sum(sol261116) == np.sum(sol15101519) == np.sum(sol36101417) == 38:
                                            # print(np.concatenate([row1, row2, row3, row4, row5]))
                                            print(np.concatenate([row1, row2, row3, row4, row5]))

@njit
def solve_r5(perms):
    # return [row5 for row5 in perms if np.sum(row5) == 38]
    for row5 in perms:
        if np.sum(row5) == 38:
            print(row5)


def solve_r4(r5):
    pieces = np.arange(1,20)
    pass
