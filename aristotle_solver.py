import numpy as np
from math import floor

class puzzle():
    def __init__(self, placements, placeType):
        # determine input mehtod
        if placeType == 'percentage':
            self.placements = placements
            
            # validate self.placements
            if len(self.placements) != 19:
                raise Exception('Expected length of placements to be 19 instead of %i' % len(self.placements))
            if sum(self.placements[i] >= 0 and self.placements[i] <= 1 for i in range(19)) != 19:
                raise Exception('All values in placements must >= 0, and <= 1')
            
            # place pieces according to percentages.
            # EXAMPLE:
            # >>>   initialPieces = [1,2,3]
            # >>>   placements = [.2, .9, .9]
            # >>>   pieces = []
            # results after first placement:
            # >>>   initialPieces 
            # [2,3]
            # >>>   pieces
            # [1]
            # results after second placement:
            # >>>   initialPieces
            # [2]
            # >>>   pieces
            # [1,3]
            self.initPieces = list(range(1,19+1)) 
            self.pieces = [self.initPieces.pop(floor(len(self.initPieces) * place)) for place in self.placements]
            del self.initPieces

        elif placeType == 'input':
            self.pieces = placements
            
            # validate self.pieces
            if sorted(self.pieces) != list(range(1,19+1)):
                raise Exception('Placements must be some arrangement of values in range(19+1)')

        else:
            raise Exception('placeType must be string "percentage" or "input"')

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
        self.ringCoords[1] = self.ringCoords[1] + self.ringCoords[1][0]  # make inner ring loopback

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
        for i in range(len(self.ringCoords[0] - 2)):
            self.newBoard[self.ringCoords[0][i+2]] = self.board[self.ringCoords[0][i]]
        # rotate inner ring
        for i in range(len(self.ringCoords[1] - 1)):
            self.newBoard[self.ringCoords[1][i+1]] = self.board[self.ringCoords[1][i]]

        self.board = self.newBoard

if __name__ == "__main__":
    pass