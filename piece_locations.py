# Generates coordinates for each puzzle piece. Check README for more details.

def populate(y, start, end):
    return [(y,i) for i in range(start, end+1, 2)]

a, b, c = populate(0,2,6)
d, e, f, g = populate(1,1,7)
h, i, j, k, l = populate(2,0,8)
m, n, o, p = populate(3,1,7)
q, r, s = populate(4,2,6)
