"""
A binary puzzle (also known as a binary Sudoku) is a puzzle played on an n × n grid;
initially some of the cells may contain 0 or 1 (but this is not the case for the 2023 competition).
One has to fill the remaining empty cells with either 0 or 1 according to the following rules:
  -  no more than two similar numbers next to or below each other are allowed,
  -  each row and each column should contain an equal number of zeros and ones,
  - each row is unique and each column is unique.

## Data
  A unique integer n

## Model
  constraints: AllDifferentList, Regular, Sum

## Execution
  python BinaryPuzzle.py -data=number
  python BinaryPuzzle.py -data=number -variant=regular

## Links
  - https://www.researchgate.net/publication/243972408_Binary_Puzzle_is_NP-complete
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
"""

from pycsp3 import *


def ref_model(param_dict):
    n = param_dict['n']
    # n = 4
    assert n % 2 == 0
    m = n // 2

    # x[i][j] is the value in the cell of the grid at coordinates (i,j)
    x = VarArray(size=[n, n], dom={0, 1})

    satisfy(
        # ensuring the same number of 0s and 1s in rows
        [Sum(x[i]) == m for i in range(n)],

        # ensuring the same number of 0s and 1s in columns
        [Sum(x[:, j]) == m for j in range(n)],

        # forbidding sequences of 3 consecutive 0s or 1s in rows
        [Sum(x[i, j:j + 3]) in range(1, 3) for i in range(n) for j in range(n - 2)],

        # forbidding sequences of 3 consecutive 0s or 1s in columns
        [Sum(x[i:i + 3, j]) in range(1, 3) for j in range(n) for i in range(n - 2)]
    )

    satisfy(
        # forbidding identical rows
        AllDifferentList(x[i] for i in range(n)),  # .to_table(),

        # forbidding identical columns
        AllDifferentList(x[:, j] for j in range(n))  # .to_table()
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
1) For XCSP competitions, before 2024, we needed to discard or translate in tables (calling .to_table())
   the AllDifferentList constraints
2) For finding a first solution, the regular model is far more efficient (at least with default heuristics)
  (a few seconds for n=50, 60 or 70)  
3) For being compatible with the competition mini-track, we use for the main variant:
   [Sum(x[i, j:j + 3]) >= 1 for i in range(n) for j in range(n - 2)],
   [Sum(x[i, j:j + 3]) <= 2 for i in range(n) for j in range(n - 2)],
4) We can write:
   [Sum(x[i, j:j + 3]) in {1,2} for i in range(n) for j in range(n - 2)], 
"""