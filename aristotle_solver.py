import numpy as np
from math import floor
from itertools import permutations, islice

class puzzle():
    def __init__(self, placements=list(range(1,20))):
        self.pieces = placements
        
        # validate self.pieces
        if sorted(self.pieces) != list(range(1,19+1)):
            raise Exception('Placements must be some arrangement of values in range(19+1)')

        # initialize variables
        # coordinates for every piece in every row on the board, starting from left most piece of the top row
        self.rowCoords = [
            [(0,i) for i in range(2,6+1,2)],
            [(1,i) for i in range(1,7+1,2)],
            [(2,i) for i in range(0,8+1,2)],
            [(3,i) for i in range(1,7+1,2)],
            [(4,i) for i in range(2,6+1,2)],
        ]

        # coordinates for every piece in every ring on the board, from outer to inner
        self.ringCoords = [
            [self.rowCoords[i][0] for i in range(0,5)] + [self.rowCoords[4][1]] + [self.rowCoords[i][-1] for i in range(4,0-1,-1)] + [self.rowCoords[0][1]],
            [self.rowCoords[i][1] for i in range(1,3+1)] + [self.rowCoords[i][-2] for i in range(3,1-1,-1)],
        ]
        self.ringCoords[0] = self.ringCoords[0] + self.ringCoords[0][:2] # make outer ring loopback
        self.ringCoords[1] = self.ringCoords[1] + [self.ringCoords[1][0]]  # make inner ring loopback

        self.board = np.zeros((5,9))    # generate empty puzzle board.        
        
        # place self.pieces onto self.board
        self.allCoords = []
        for row in self.rowCoords:
            self.allCoords += row
        self.coords = zip(self.pieces, self.allCoords)
        for pair in self.coords:
            self.board[pair[1]] = pair[0]

    def check_row_sums(self):
        return [sum(self.board[i]) == 38 for i in range(0, self.board.shape[0])]

    def rotate_board(self):
        self.newBoard = np.zeros((5,9))        
        # NOTE: rotation can be done using self.ringCoords as a map, and shifting self.board[ring[i]] to self.board[ring[i+2]] 
        # NOTE: i+2 for outer ring, i+1 for inner ring

        # rotate outer ring
        for i in range(len(self.ringCoords[0]) - 2):
            self.newBoard[self.ringCoords[0][i+2]] = self.board[self.ringCoords[0][i]]
        # rotate inner ring
        for i in range(len(self.ringCoords[1]) - 1):
            self.newBoard[self.ringCoords[1][i+1]] = self.board[self.ringCoords[1][i]]

        self.board = self.newBoard

    def validate(self):
        self.tests = self.check_row_sums()
        self.rotate_board()
        self.tests += self.check_row_sums()
        self.rotate_board()
        self.tests += self.check_row_sums()
        return all(self.tests)

    def reset(self, placements):
        self.__init__(placements)

def brute_force(skipTo=0, notifyPer=1000):
    # create permutations generator
    perms = permutations(list(range(1,19+1)), 19)
    # skip n permutations
    if skipTo != 0:
        perms = islice(perms, skipTo, None)
    
    newBoard = puzzle()

    for perm in perms:
        newBoard.reset(perm)
        if newBoard.validate():
            return {'solution': perm, 'iteration': skipTo}
        else:
            skipTo += 1
            if skipTo % notifyPer == 0:
                print(skipTo, ' iterations.')
    return 'No solution.'

if __name__ == "__main__":
    brute_force()