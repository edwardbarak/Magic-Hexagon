import piece_locations as ploc 
import numpy as np

def validate(*args):
    pass

def check_horizontal_rows(df):
    checks = []
    for i in range(df.shape[0]):
        checks.append(sum(df[i]) == 38)
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




df = np.zeros((5,9))
pieces = list(range(1,19+1))
