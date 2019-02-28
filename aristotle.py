import numpy as np
import math

"""
def generateProbabilities(unitType, units):
    # generate an array of probabilities, with length = num of pieces in final hexagon. 
    # As of now, this function is not yet required, and should be removed during the next refactoring.
    unitTypeError = 'Argument "unitType" must be string "pieces" or "radius"'
    unitType = unitType.lower()
    unitTypeOptions = ['pieces', 'radius']
    if unitType in unitTypeOptions:
        if unitType == 'pieces':
        # TODO: return  
        elif unitType == 'radius':
        # TODO: 
    else:
        raise Exception(unitTypeError)
"""

def hexagonRadius(probabilities):
    piecesError = 'Improper number of pieces to create a hexagon'
    pieces = len(probabilities)
    
    a = 3
    b = 3
    c = -1 * (pieces-1)

    # Quadratic equation to solve hexagon radius. Units is number of hexagons
    # calculate the discriminant
    d = (b**2) - (4*a*c)
    
    # find radius
    solutions = [(-b-math.sqrt(d))/(2*a), (-b+math.sqrt(d))/(2*a)]
    positiveSolutions = [i for i in solutions if i >= 0]
    isPositiveInt = [i % 1 == 0 for i in positiveSolutions]
    if True in isPositiveInt:
        radius = positiveSolutions[isPositiveInt.index(True)]
        return radius
    else:
        raise Exception(piecesError)

def hexagonRadiusToPieces(radius):
    """Radius of final hexagon is determined by how many pieces does it take in one direction to get to the edge of the final hexagon? Excluding the center piece.

    Examples:
    (hexagon radius, hexagon pieces)
    (0, 1)  Only the center piece
    (1, 7)  6 pieces adjacent to the center piece
    (2, 19) Configuration of final hexagon in Aristotle's puzzle
    """
    r = radius
    return 3 * r * (r + 1) + 1

def validate(probabilities, shape=(5,9), ans=38):
    # TODO: Extrapolate shape and ans from len(probabilities), then remove function arguments shape and ans.

    #  ERROR CHECKING:
    ## probabilities must be of type list
    ## length of probabilities must correspond with the number of pieces in the puzzle
    if not isinstance(probabilities, list): 
        raise Exception('Argument "probabilities" must be of type list.')
    if not isinstance(shape, tuple):
        raise Exception('Argument "shape" must be of type tuple.')
    if len(probabilities) != 19: print('WARNING: Probabilities list is not of default length 19')
    if ans != 38: print('WARNING: ans is not set to the default value of 38')
    
    # change 100% probabilities to 99.99% probabilities to avoid IndexError
    for val in range(0, len(probabilities)):
        if probabilities[val] == 1: probabilities[val] = .9999

    initialPieces = list(range(1,len(probabilities)+1)) # generate puzzle pieces
    selectedPieces = []

    # select pieces to place
    for prob in probabilities:
        selectionIndex = math.floor(prob*len(initialPieces))
        selectedPieces.append(initialPieces.pop(selectionIndex))

    # place selected pieces onto board
    df = np.zeros(shape)
    centerPiece = math.ceil(len(probabilities)/2)
    # TODO: map locations of selectedPieces to df
    

def check_horizontal_rows(df, ans):
    checks = []

    for i in range(df.shape[0]):
        checks.append(sum(df[i]) == ans)
    return checks

def check_diag_rows(df, direction, ans):
    checks = []
    direction = direction.lower()
    directionError = 'Direction must be either "ul" (up left) or "ur" (up right)'
    
    # 1.   Check y value of first value from the {ul: right, ur: left}
    # 2.   Second and subsequent values are {ul: (-1,1), ur: (1,1)} of the previous value, until y value's ceiling is reached
    # 3.   Then each subsequent value is {ul: (-2,0), ur: (2,0)} from the previous value, until the next subsequent value is 0 OR reached x floor/ceiling
    
    # Step 1. 
    if direction not in ['ul','ur']: raise Exception(directionError)
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
        raise Exception(directionError)

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
    direction = direction.lower()
    nums = []

    directionError = 'Direction must be either "ul" (up left) or "ur" (up right)'
    if direction == 'ul': 
        xstep = 1
    elif direction == 'ur': 
        xstep = -1
    else: 
        raise Exception(directionError)
       
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
