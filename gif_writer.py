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

    STATES = 2
    #NEIGHBORHOOD = 'Moore'
    RADIUS = 1
    ROWS = 120
    COLUMNS = 120

    CENTER = 3
    CENTER_PROPORTION = .7
    H_MIRROR = 1
    V_MIRROR = 2

    #COLOR_MAP = cm.BW
    COLOR_MAP = cm.random_cmap(STATES, SEED)
    CELL_SIZE = 7
    GENERATIONS = 100
    FRAME_DELAY = .1

    initial_state = inits.random_state(rows=ROWS, columns=COLUMNS, states=STATES, seed=SEED, center=CENTER, p=CENTER_PROPORTION, h_mirror=H_MIRROR, v_mirror=V_MIRROR)
    #updater = ufuns.random_update_function(states=STATES, seed=SEED)
    updater = ufuns.preset('BLINKY1')
    #ruledict = updater.ruledict

    boardstates = updater(initial_state)

    frames = frame_generator(boards=boardstates, cell_size=CELL_SIZE, color_map=COLOR_MAP)

    def get_frame(dummy):
        return next(frames)

    moviepy.editor.VideoClip(get_frame, duration=GENERATIONS*FRAME_DELAY).write_gif(FILENAME, fps=1/FRAME_DELAY)


def frame_generator(boards=None, cell_size=10, color_map=None):
    
    if not isinstance(color_map, GeneratorType): color_map = repeat(color_map)

    for B in boards:
        frame = np.zeros([cell_size*d for d in B.shape]+[3], dtype=np.uint8)
        for row in range(B.shape[0]):
            for column in range(B.shape[1]):
                frame[cell_size*row:cell_size*(row+1), cell_size*column:cell_size*(column+1)] = next(color_map)[B[row,column]]
        yield frame


if __name__=='__main__':
    main()