"""
The famous logic puzzle. See, e.g., "Sudoku as a Constraint Problem" by Helmut Simonis

## Data Example
  s13a.json

## Model
  There exists different variant.

  constraints: AllDifferent, Sum, Table

## Execution:
  python Sudoku.py -data=[number,None]
  python Sudoku.py -data=<datafile.json>
  python Sudoku.py -data=<datafile.json> -variant=table
  python Sudoku.py -data=<datafile.txt> -parser=Sudoku_Parser.py

## Links
 - https://en.wikipedia.org/wiki/Sudoku
 - https://www.semanticscholar.org/paper/Sudoku-as-a-Constraint-Problem-Simonis/4f069d85116ab6b4c4e6dd5f4776ad7a6170faaf

## Tags
  recreational, notebook
"""

import math
from pycsp3 import *

def ref_model(param_dict):
    n = param_dict['n']
    clues = param_dict['clues']

    # n, clues = data_["n"], data_["clues"]  # n (order of the grid) is typically 9 -- if not 0, clues[i][j] is a value imposed at row i and col j
    base = int(math.sqrt(n))
    assert base * base == n

    # x[i][j] is the value of cell with coordinates (i,j)
    x = VarArray(size=[n, n], dom=range(1, n + 1))

    ## @variants removed
    satisfy(
        # imposing distinct values on each row and each column
        AllDifferent(x, matrix=True),

        # imposing distinct values on each block  tag(blocks)
        [AllDifferent(x[i:i + base, j:j + base]) for i in range(0, n, base) for j in range(0, n, base)]
    )
    #
    satisfy(
        # imposing clues  tag(clues)
        x[i][j] == clues[i][j] 
        for i in range(n) 
        for j in range(n) 
        if clues and clues[i][j] > 0
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
1) Using set(permutations(range(1, n + 1))) instead of list(permutations(range(1, n + 1))) is far less time-efficient

2) opt is used in the 2022 Minizinc Challenge
"""