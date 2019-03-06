import numpy as np
from math import floor

class puzzle(placements, placeType):
    rowCoords = [
        [(0,i) for i in range(2,6+1,2)],
        [(1,i) for i in range(1,7+1,2)],
        [(2,i) for i in range(0,8+1,2)],
        [(3,i) for i in range(1,7+1,2)],
        [(4,i) for i in range(2,6+1,2)],
    ]
    ringCoords = [
        [rowCoords[i][0] for i in range(0,5)] + [rowCoords[4][1]] + [rowCoords[i][-1] for i in range(4,0-1,-1)] + [rowCoords[0][1]],
        [rowCoords[i][1] for i in range(1,3+1)] + [rowCoords[i][-2] for i in range(3,1-1,-1)],
    ]
    
    def __init__(self, placements, placeType):
        if placeType == 'percentage':
            self.placements = placements
            
            # validate self.placements
            if len(self.placements) != 19:
                raise Exception('Expected length of placements to be 19 instead of %i' % len(self.placements))
            if sum(self.placements[i] >= 0 and self.placements[i] <= 1 for i in range(19)) != 19:
                raise Exception('All values in placements must >= 0, and <= 1')
            
            self.initPieces = list(range(1,19+1)) 
            self.pieces = [self.initPieces.pop(floor(len(self.initPieces) * place)) for place in self.placements]
            del self.initPieces

        elif placeType == 'input':
            self.pieces = placements
            
            # validate self.pieces
            if sorted(self.pieces) != list(range(19+1)):
                raise Exception('Placements must be some arrangement of values in range(19+1)')

        else:
            raise Exception('placeType must be string "percentage" or "input"')

        self.board = np.zeros((5,9))

    def check_row_sums(self):
        return [sum(self.board[i]) == 38 for i in range(0, self.board.shape[0])]

    # TODO: Write this function
    def rotate_board(self):
        newBoard = np.zeros((5,9))
        rotateInstr = zip()