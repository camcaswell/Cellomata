from sys import exit
import numpy as np
from math import floor, ceil

if __name__=='__main__':
	exit('Oops, you ran the wrong file.')


def random_state(rows=10, columns=10, states=2, seed=None, center=0, p=.25, h_mirror=0, v_mirror=0):
 
    ''' The mirror parameters denote how many times you want the random sub-board mirrored horizontally and vertically.
        The center parameter is on which recursion level you want the board to be centered in a white border (1 for top-level).
        *p* is the proportion of the sidelength for the center block.
    '''

    center = min(h_mirror+v_mirror+1, center)

    if center == 1:
        state = np.zeros((rows,columns), dtype=np.uint8)
        rstart = ceil( (rows-1)/2 - (p*rows-1)/2 )
        rend =  floor( (rows-1)/2 + (p*rows-1)/2 )
        cstart = ceil( (columns-1)/2 - (p*columns-1)/2 )
        cend =  floor( (columns-1)/2 + (p*columns-1)/2 )
        state[rstart:rend+1, cstart:cend+1] = random_state(rows=rend-rstart+1, columns=cend-cstart+1, states=states, seed=seed, h_mirror=h_mirror, v_mirror=v_mirror)
        return state

    elif h_mirror:
        half_state = random_state(rows=rows, columns=(columns+1)//2, states=states, seed=seed, center=center-1, p=p, h_mirror=h_mirror-1, v_mirror=v_mirror)
        return np.concatenate((half_state, np.flip(half_state, 1)[columns%2:]), 1)

    elif v_mirror:
        half_state = random_state(rows=(rows+1)//2, columns=columns, states=states, seed=seed, center=center-1, p=p, h_mirror=h_mirror, v_mirror=v_mirror-1)
        return np.concatenate((half_state, np.flip(half_state, 0)[rows%2:]), 0)

    else:
        np.random.seed(seed)
        return np.random.randint(low=0, high=states, size=(rows, columns), dtype=np.uint8)
