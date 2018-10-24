import numpy as np
from math import sqrt

if __name__=='__main__': 
    exit('Oops, you ran the wrong file.')

def cmformat(*args):
    ''' formats a color map as a list of 1x1x3 ndarrays
    '''
    return [np.array(v, dtype=np.uint8).reshape(1,1,3) for v in args]

def clr_dist(ray,vec):
    ray = np.squeeze(ray).astype(np.int)
    vec = np.squeeze(vec).astype(np.int)
    m = np.linalg.norm(vec)/np.linalg.norm(ray)
    shade_dif = abs(np.linalg.norm(ray)-np.linalg.norm(vec))
    offset = sqrt(sum((m*ray-vec)**2))
    return shade_dif, offset

def random_cmap(count=2, seed=None):
    ''' generates a map of *count* random RGB vectors
    '''
    np.random.seed(seed)
    return [np.random.randint(0,255,(1,1,3),np.uint8) for idx in range(count)]

def random_lc_cmap(count=2, seed=None):
    retmap = [np.random.randint(0,255,(1,1,3),np.uint8)]
    print(retmap[0])
    while count>1:
        clr = np.random.randint(0,255,(1,1,3),np.uint8)
        shade_dif, offset = clr_dist(retmap[0], clr)
        if 35<shade_dif<150 and 35<offset<100:
            retmap.append(clr)
            count -= 1
            print(clr, clr_dist(retmap[0], clr))
    return retmap

## RGB values should be 0-255

BW = cmformat([255, 255, 255], [0,0,0])