"""
It is a kind of logic puzzle. See "Kakuro as a Constraint Problem" by Helmut Simonis.

## Data Example
  easy-000.json

## Model
 constraints: AllDifferent, Sum, Table

## Execution
  python Kakuro.py -data=<datafile.jon>
  python Kakuro.py -data=<datafile.jon> -variant=table

## Links
 - https://en.wikipedia.org/wiki/Kakuro
 - https://www.researchgate.net/publication/228524341_Kakuro_as_a_Constraint_Problem

## Tags
  recreational
"""

from pycsp3 import *
from pycsp3.tools.curser import convert_to_namedtuples

# n, m, clues = data


def ref_model(param_dict):
    n = param_dict['nRows']
    m = param_dict['nCols']
    row_clues = convert_to_namedtuples({"r":param_dict['row_clues']}).r 
    col_clues = convert_to_namedtuples({"c":param_dict['col_clues']}).c 
    # n, m, row_clues, col_clues = data

    Cells = [(i, j) for i in range(n) for j in range(m)]
    # x[i][j] is the value put at row i and column j
    x = VarArray(size=[n, m], dom=lambda i, j: range(1, 10) if row_clues[i][j] == col_clues[i][j] == 0 else None)

    # Two useful arrays for posting easily constraints
    horizontal = [(x[i][j + 1:next((k for k in range(j + 1, m) if row_clues[i][k] != 0), m)], v) for i, j in Cells if (v := row_clues[i][j]) > 0]
    vertical = [(x[i + 1:next((k for k in range(i + 1, n) if col_clues[k][j] != 0), n), j], v) for i, j in Cells if (v := col_clues[i][j]) > 0]

    satisfy(
        [Sum(scp) == v for (scp, v) in horizontal],

        [AllDifferent(scp) for (scp, _) in horizontal],

        [Sum(scp) == v for (scp, v) in vertical],

        [AllDifferent(scp) for (scp, _) in vertical]
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