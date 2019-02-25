import aristotle.piece_locations as ploc 
import numpy as np

def validate(*args):
    pass

def check_horizontal_rows(df, ans):
    checks = []
    for i in range(df.shape[0]):
        checks.append(sum(df[i]) == ans)
    return checks

def check_diag_rows(df, direction):
    directionError = 'Direction must be either "ul" (up, left) or "ur" (up, right)'
    # Check what the diagonal direction is
    if direction not in ['ul','ur']: raise(ValueError, directionError)
    if direction == 'ul':
        step = 1
        xstart = 0
        xend = df.shape[1]
    elif direction == 'ur':
        step = -1
        xstart = df.shape[1]
        xend = -1 # 0 - 1 = -1
    else:
        raise(ValueError, directionError)

    # 


### VARIABLES ###
ans = 38            # value that each row needs to sum up to
x = 5               # number of horizontal rows
y = x * 2 - 1       # number of columns after spacing out values
numOfPieces = 19    # number of pieces given in the puzzle

### MAIN ###
df = np.zeros((x,y))
pieces = list(range(1, numOfPieces+1))
