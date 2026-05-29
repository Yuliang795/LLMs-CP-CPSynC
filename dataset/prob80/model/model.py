"""
A logic puzzle video game.

## Data
  no JSON file for the moment

## Model
  constraints: Sum

## Execution:
  python MineSweeper.py
  python MineSweeper.py -data=<datafile.json>

## Links
 - https://en.wikipedia.org/wiki/Minesweeper_(video_game)

## Tags
  recreational
"""

from pycsp3 import *

def ref_model(param_dict):
    puzzle = param_dict['puzzle']
    n, m = len(puzzle), len(puzzle[0])
    #
    # 4 solutions

    # x[i][j] is 1 iff there is a mine in the square at row i and column j
    x = VarArray(size=[n, m], dom=lambda i, j: {0} if puzzle[i][j] >= 0 else {0, 1})

    satisfy(
        # respecting clues of the puzzle
        Sum(x.around(i, j)) == puzzle[i][j] for i in range(n) for j in range(m) if puzzle[i][j] >= 0
    )
    #
    return x


#################
import sys, os
UTIL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../utils'))
if UTIL_PATH not in sys.path:
    sys.path.insert(0, UTIL_PATH)
from io_helper import load_inputs

import argparse, pickle
from ovar_transformer import ovar_transformer
if __name__ == '__main__':
    #
    args, param_dict, dvar_dict = load_inputs(ovar_transformer)
    #
    x = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

""" Comments
1) around() is a predefined method on matrices of variables (of type ListVar).
   Hence, x.around(i, j) is equivalent to :
   [x[i + k][j + l] for k in [-1, 0, 1] for l in [-1, 0, 1] if 0 <= i + k < n and 0 <= j + l < m and (k, l) != (0, 0)]
"""