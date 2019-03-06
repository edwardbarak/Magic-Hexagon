import numpy as np
import math

def check_row_sums(board):
    return [sum(board[i]) == 38 for i in range(0, board.shape[0])]

# TODO: Write this function
def rotate_board(board):
    newBoard = np.zeros((5,9))
    transposeInstr = zip()

board = np.zeros((5,9))
pieces = list(range(1,19+1))
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
