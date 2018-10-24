from numpy import array, uint8, random

if __name__=='__main__': 
    exit('Oops, you ran the wrong file.')

def cmformat(*args):
    ''' formats a color map as a list of 1x1x3 ndarrays
    '''
    return [array(v, dtype=uint8).reshape(1,1,3) for v in args]

def random_cmap(count=2, seed=None):
    ''' generates a map of *count* random RGB vectors
    '''
    random.seed(seed)
    return [random.randint(0,255,(1,1,3),uint8) for idx in range(count)]

## RGB values should be 0-255

BW = cmformat([255, 255, 255], [0,0,0])