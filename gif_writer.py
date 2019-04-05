import initial_states as inits
import update_functions as ufuns
import cmap as cm

import moviepy.editor
import numpy as np
from itertools import repeat
from types import GeneratorType
import os

def main():

    name_attempt = 'test' + '.gif'
    count = 1
    while name_attempt in os.listdir():
        count += 1
        name_attempt = f'{FILENAME} {count}'
    FILENAME = name_attempt

    SEED = None

    STATES = 3
    #NEIGHBORHOOD = 'Moore'
    #RADIUS = 1
    ROWS = 50
    COLUMNS = 50
 
    CENTER = 0
    CENTER_PROPORTION = .9
    H_MIRROR = 0
    V_MIRROR = 0

    #COLOR_MAP = cm.preset('WEEN')
    COLOR_MAP = cm.random_cmap(STATES, SEED)
    CELL_SIZE = 10
    GENERATIONS = 100
    FRAME_DELAY = .2


    initial_state = inits.random_state(ROWS, COLUMNS, STATES, SEED, CENTER, CENTER_PROPORTION, H_MIRROR, V_MIRROR)

    updater = ufuns.random_update_function(states=STATES, seed=SEED, stability=.69)
    #updater = ufuns.preset('BLINKY_ORDER')

    boardstates = updater(initial_state)

    frames = frame_generator(boards=boardstates, color_map=COLOR_MAP, cell_size=CELL_SIZE)

    # The moviepy gif writer function requires a function that returns frames for a given time index.
    # This function takes a time index, ignores it, and passes the next frame.
    def get_frame(dummy):
        return next(frames)

    moviepy.editor.VideoClip(get_frame, duration=GENERATIONS*FRAME_DELAY).write_gif(FILENAME, fps=1/FRAME_DELAY)

def frame_generator(boards, color_map, cell_size=10):
    
    if not isinstance(color_map, GeneratorType): color_map = repeat(color_map)

    for B in boards:
        frame = np.zeros([cell_size*d for d in B.shape]+[3], dtype=np.uint8)
        for row in range(B.shape[0]):
            for column in range(B.shape[1]):
                frame[cell_size*row:cell_size*(row+1), cell_size*column:cell_size*(column+1)] = next(color_map).vecs()[B[row,column]]
        yield frame

def gen_no_write(get_frame, g):
    ''' Just for speed testing
    '''
    for i in range(g):
        get_frame(g)


if __name__=='__main__':
    main()