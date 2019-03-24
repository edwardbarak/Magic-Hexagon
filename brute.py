#!/usr/bin/env pypy3

from itertools import permutations
from time import time

start = time()
allPieces = set(range(1,20))

try:
    solutions = (solution for solution in permutations(allPieces, 19) if not False in iter((
        # horizontal sums
        sum(solution[:3]) == 38,
        sum(solution[4:8]) == 38,
        sum(solution[8:13]) == 38,
        sum(solution[13:17]) == 38,
        sum(solution[17:]) == 38,
        # top right to bottom left diagonal sums
        sum(((solution[x] for x in (0,3,7)))) == 38,
        sum(((solution[x] for x in (1,4,8,12)))) == 38,
        sum(((solution[x] for x in (2,5,9,13,16)))) == 38,
        sum(((solution[x] for x in (6,10,14,17)))) == 38,
        sum(((solution[x] for x in (11,15,18)))) == 38,
        # top left to bottom right diagonal sums
        sum(((solution[x] for x in (7,12,16)))) == 38,
        sum(((solution[x] for x in (3,8,13,17)))) == 38,
        sum(((solution[x] for x in (0,4,9,14,18)))) == 38,
        sum(((solution[x] for x in (1,5,10,15)))) == 38,
        sum(((solution[x] for x in (2,6,11)))) == 38))
    )

    print('Solution 1:')
    print(solutions.__next__())

    print('\nSolution Count: %s' % (sum((1 for i in solutions)) + 5))
    print('Time: %s' % (time() - start))
except KeyboardInterrupt:
    print('\nTime: %s' % (time() - start))