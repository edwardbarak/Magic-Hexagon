import aristotle.piece_locations as ploc 
import numpy as np
import math

def validate(probabilities):
    # probabilities must be of type list
    # 
    if not isinstance(probabilities, list): 
        raise(TypeError, 'Argument "probabilities" must be of type list.')
    
    pieces = list(range(1,len(probabilities)+1))

def check_horizontal_rows(df, ans):
    checks = []

    for i in range(df.shape[0]):
        checks.append(sum(df[i]) == ans)
    return checks

def check_diag_rows(df, direction, ans):
    checks = []
    directionError = 'Direction must be either "ul" (up left) or "ur" (up right)'
    
    # 1.   Check y value of first value from the {ul: right, ur: left}
    # 2.   Second and subsequent values are {ul: (-1,1), ur: (1,1)} of the previous value, until y value's ceiling is reached
    # 3.   Then each subsequent value is {ul: (-2,0), ur: (2,0)} from the previous value, until the next subsequent value is 0 OR reached x floor/ceiling
    
    # Step 1. 
    if direction not in ['ul','ur']: raise(ValueError, directionError)
    if direction == 'ul':
        diagStep = -1
        horizStep = -2
        xstart = 0
        xend = df.shape[1]
    elif direction == 'ur':
        diagStep = 1
        horizStep = 2
        xstart = df.shape[1]
        xend = -1 # 0 - 1 = -1
    else:
        raise(ValueError, directionError)

    ystart = math.floor(df.shape[0] / 2) # Find first y value. First y value is always going to be floor of df.shape[0]/2, which is the center y coordinate
    
    # Step 2.
    for i in range(ystart, df.shape[0]+1):
        checks.append(diag_row_sum(i, x, df, direction, ans))
        x += xstep

    # Step 3.
    for i in range(x, xend + xstep, horizStep):
        checks.append(diag_row_sum(df.shape[0], i, direction, ans))

    return checks

def diag_row_sum(y, x, df, direction, ans):
    # Sums up a diagonal row
    nums = []

    directionError = 'Direction must be either "ul" (up left) or "ur" (up right)'
    if direction == 'ul': 
        xstep = 1
    elif direction == 'ur': 
        xstep = -1
    else: 
        raise(ValueError, directionError)
       
    for i in range(y, 0 - 1, -1):
        nums.append(df[i,x])
        x += xstep

    return sum(nums) == ans


### VARIABLES ###
ans = 38            # value that each row needs to sum up to
x = 5               # number of horizontal rows
y = x * 2 - 1       # number of columns after spacing out values
numOfPieces = 19    # number of pieces given in the puzzle

### MAIN ###
df = np.zeros((x,y))
pieces = list(range(1, numOfPieces+1))