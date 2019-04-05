import cmap as cm
import update_functions as ufuns
import initial_states as inits

import moviepy.editor
from itertools import repeat
from types import GeneratorType
import numpy as np

from time import time

def main():
    SEED = 8
    STATES = 3
    FRAME_DELAY = .05
    CELL_SIZE = 10
    GENERATIONS = 250

    COLOR_MAP = cm.random_cmap(STATES, seed=SEED)
    initial_state = inits.random_state(100, 100, STATES, seed=SEED)
    updater1 = ufuns.random_update_function(states=STATES, seed=SEED)
    updater2 = ufuns.random_update_function(states=STATES, seed=SEED, alt=True)

    framegen1 = frame_generator(updater1(initial_state), COLOR_MAP, CELL_SIZE)
    framegen2 = frame_generator(updater2(initial_state), COLOR_MAP, CELL_SIZE)

    def frame_iter1(i):
        return next(framegen1)
    def frame_iter2(i):
        return next(framegen2)

    # mark0 = time()
    # moviepy.editor.VideoClip(frame_iter1, duration=GENERATIONS*FRAME_DELAY).write_gif("speedtest.gif", fps=1/FRAME_DELAY)
    # mark1 = time()
    # print(f"Wrote gif in {mark1-mark0:.1f} seconds.\n")

    mark0 = time()
    for i in range(GENERATIONS):
        frame_iter1(i)
    mark1 = time()
    print(f"Generated {GENERATIONS} frames in {mark1-mark0:.1f} seconds.")

    mark2 = time()
    for i in range(GENERATIONS):
        frame_iter2(i)
    mark3 = time()
    print(f"Generated {GENERATIONS} frames in {mark3-mark2:.1f} seconds.")



def frame_generator(boards, color_map, cell_size=10):
    
    if not isinstance(color_map, GeneratorType): color_map = repeat(color_map)

    for B in boards:
        frame = np.zeros([cell_size*d for d in B.shape]+[3], dtype=np.uint8)
        for row in range(B.shape[0]):
            for column in range(B.shape[1]):
                frame[cell_size*row:cell_size*(row+1), cell_size*column:cell_size*(column+1)] = next(color_map).vecs()[B[row,column]]
        yield frame


if __name__=="__main__":
    main()