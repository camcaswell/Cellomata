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
WB = cmformat([0,0,0], [255, 255, 255])
LEAFLIFE = cmformat([182, 249, 214], [131, 209, 94])

HARVEST = cmformat([197, 77, 0], [155, 207, 81], [252, 196, 0])
FARHARVEST = cmformat([58, 124, 97], [241, 227, 24], [220, 38, 8])
OLDSAND = cmformat([248, 216, 110], [161, 59, 17], [223, 117, 0])
ALGAE = cmformat([129, 199, 144], [19, 148, 235], [161, 232, 255])
CARROTFIELD = cmformat([221, 103, 16], [68, 123, 45], [109, 106, 44])
FRIENDLYVOID = cmformat([82, 116, 254], [185, 229, 239], [218, 104, 0])
COLDFUSION = cmformat([46, 7, 225], [0, 255, 111], [109, 225, 241])
LIGHTABYSS = cmformat([51, 57, 242], [121, 116, 242], [23, 55, 154])
LABLIFE = cmformat([208, 62, 153], [46, 162, 39], [154, 255, 189])