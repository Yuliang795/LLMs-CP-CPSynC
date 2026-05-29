"""
In a Survo puzzle, the task is to fill an m × n table with integers 1, 2, ..., m·n
so that each of these numbers appears only once and their row and column sums
are equal to integers given on the bottom and the right side of the table.
Often some of the integers are given readily in the table in order to guarantee
uniqueness of the solution and/or for making the task easier.

## Data Example
  01.json

## Model
  constraints: AllDifferent, Sum

## Execution:
  python Survo.py -data=<datafile.json>

## Links
 - https://en.wikipedia.org/wiki/Survo_puzzle

## Tags
  recreational
"""

from pycsp3 import *



def ref_model(param_dict):
    r_sums, c_sums, matrix = param_dict["rowSums"], param_dict["colSums"], param_dict["matrix"]
    m, n = param_dict["m"], param_dict["n"]

    # x[i][j] is the value in the cell at row i and column j
    x = VarArray(size=[m, n], dom=range(1, m * n + 1))

    satisfy(
        # taking hints into consideration
        [x[i][j] == matrix[i][j] for i in range(m) for j in range(n) if matrix[i][j] != 0],

        # all numbers must appear once
        AllDifferent(x),

        # respecting sums on rows
        [Sum(x[i]) == r_sums[i] for i in range(m)],

        # respecting sums on columns
        [Sum(x[:, j]) == c_sums[j] for j in range(n)]
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