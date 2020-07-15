#!/usr/bin/env python3

"""
Generate sudoku boards to the static/sudoku_boards directory.
"""

import os
import shutil
from sudoku_manager.sudoku import Sudoku

static_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..',
    'static',
    'sudoku_boards'
)

shutil.rmtree(static_dir)
os.makedirs(static_dir, exist_ok=True)

for i in range(1, 6):
    print(f'Generating {Sudoku.DIFFICULTIES[i]["name"]} boards...')
    output_dir = os.path.join(static_dir, Sudoku.DIFFICULTIES[i]["name"])
    os.makedirs(output_dir, exist_ok=True)
    for j in range(1000):
        if j % 10 == 0:
            print('.', flush=True, end='')
        Sudoku.generate_grid(i, os.path.join(output_dir, f'{j+1}.json'), True)
    print('')
