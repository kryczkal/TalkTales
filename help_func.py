import numpy as np

def factorize(x: int):
    val = int(np.sqrt(x))

    if (val ** 2 == x):
        return (val, val)
    
    if (x%2 == 1):
        shift = -2
    else:
        shift = -1

    for i in range(val, 1,shift):
        if (x % float(i) == 0):
            return (i, int(x/i))

