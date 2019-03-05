import numpy as np
import math

def checkRowSums(board):
    return [sum(board[i]) == 38 for i in range(0, board.shape[0])]

# TODO: Write this function
def rotateBoard(board):
    newBoard = np.zeros((5,9))


board = np.zeros((5,9))
pieces = list(range(1,19+1))
coords = {
        'row0': [(0,i) for i in range(2,6+1,2)],
        'row1': [(1,i) for i in range(1,7+1,2)],
        'row2': [(2,i) for i in range(0,8+1,2)],
        'row3': [(3,i) for i in range(1,7+1,2)],
        'row4': [(4,i) for i in range(2,6+1,2)],
        }

