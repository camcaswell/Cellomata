import initial_states as inits
import update_functions as ufuns
import cmap as cm

import moviepy.editor
import numpy as np
from itertools import repeat
from types import GeneratorType

def main():

    FILENAME = 'test' + '.gif'

    SEED = None

    STATES = 3
    #NEIGHBORHOOD = 'Moore'
    #RADIUS = 1
    ROWS = 100
    COLUMNS = 100

    CENTER = 0
    CENTER_PROPORTION = .95
    H_MIRROR = 0
    V_MIRROR = 0

    COLOR_MAP = cm.preset('FRIENDLYVOID')
    #COLOR_MAP = cm.random_cmap(STATES, SEED)
    CELL_SIZE = 5
    GENERATIONS = 20
    FRAME_DELAY = .02

    initial_state = inits.random_state(ROWS, COLUMNS, STATES, SEED, CENTER, CENTER_PROPORTION, H_MIRROR, V_MIRROR)

    updater = ufuns.random_update_function(states=STATES, seed=SEED, stability=.75)
    #updater = ufuns.preset('RIGRID')
    #ruledict = updater.ruledict

    boardstates = updater(initial_state)

    frames = frame_generator(boards=boardstates, color_map=COLOR_MAP, cell_size=CELL_SIZE)

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
    for i in range(g):
        get_frame(g)


if __name__=='__main__':
    main()