import numpy as np
from math import sqrt
from configparser import ConfigParser
from ast import literal_eval 

if __name__=='__main__': 
    exit('Oops, you ran the wrong file.')

class cmap:

    def __init__(self, first, *args):
        ''' Accepts a list of numpy.ndarrays, multiple ndarrays, a list of lists of RGB values, or multiple lists of RGB values.
            RGB values are assumed to be 0-255 unless floats in 0-1 are passed. They are stored as 0-255 ints.
        '''
        if args:
            if isinstance(first, np.ndarray):
                self.clrlist = [v.reshape(3).tolist() for v in [first]+list(args)]
            else:
                self.clrlist = [first]+list(args)
        else:
            if isinstance(first[0], np.ndarray):
                self.clrlist = [v.reshape(3).tolist() for v in first]
            else:
                self.clrlist = first

        for idx,color in enumerate(self.clrlist):
            if isinstance(color[0], (np.integer, int)):
                intedcolor = [int(x) for x in color]
            elif isinstance(color[0], (np.floating, float)):
                if False not in [0<=x<=1 for x in color]:
                    intedcolor = [int(256*x) for x in color]
                else:
                    intedcolor = [int(x) for x in color]
            if False not in [isinstance(x,int) and 0<=x<=255 for x in intedcolor]:
                self.clrlist[idx] = intedcolor
            else:
                raise ValueError("Input a list of numpy.ndarrays, multiple ndarrays, a list of lists, or multiple lists of RGB values.\nRGB values should be ints in 0-255 or floats in 0-1.")

    def __str__(self):
        return str(self.clrlist)

    def vecs(self):
        return [np.array(v, dtype=np.uint8).reshape(1,1,3) for v in self.clrlist]


def random_cmap(count=2, seed=None):
    ''' Generates a cmap of *count* random RGB vectors
    '''
    np.random.seed(seed)
    retcmap = cmap([np.random.randint(0,255,3) for idx in range(count)])

    config_writer = ConfigParser()
    with open('Last_Random.cfg', 'r') as savefile:
        config_writer.read_file(savefile)
        config_writer.set('Color Map', 'cmap', str(retcmap))
    with open('Last_Random.cfg', 'w') as savefile:
        config_writer.write(savefile)

    return retcmap

def random_lc_cmap(count=2, seed=None):
    ''' Generates a cmap of *count* random RGB vectors where each vector is "close" to the first one.
        See clr_dist() for what "close" means.
    '''
    firstcolor = np.random.randint(0,255,3)
    retlist = [firstcolor]
    while count>1:
        trialcolor = np.random.randint(0,255,3)
        shade_dif, offset = clr_dist(firstcolor, trialcolor)
        if 35<shade_dif<150 and 35<offset<100:
            retlist.append(trialcolor)
            count -= 1
    retcmap = cmap(retlist)

    config_writer = ConfigParser()
    with open('Last_Random.cfg', 'r') as savefile:
        config_writer.read_file(savefile)
        config_writer.set('Color Map', 'cmap', str(retcmap))
    with open('Last_Random.cfg', 'w') as savefile:
        config_writer.write(savefile)

    return retcmap

def preset(name):
    with open('Preset_Colors.cfg') as savefile:
        preset_reader = ConfigParser()
        preset_reader.read_file(savefile)
        preset_clr = literal_eval(preset_reader.get(name, 'cmap'))
    return cmap(preset_clr)

def clr_dist(ray,vec):
    ray = np.squeeze(ray).astype(np.int)
    vec = np.squeeze(vec).astype(np.int)
    m = np.linalg.norm(vec)/np.linalg.norm(ray)
    shade_dif = abs(np.linalg.norm(ray)-np.linalg.norm(vec))
    offset = sqrt(sum((m*ray-vec)**2))
    return shade_dif, offset