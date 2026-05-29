"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The original MZN model was proposed by Krzysztof Kuchcinski, and data come from the paper cited below.
The licence seems to be like a MIT Licence.

## Data Example
  057.json

## Model
  constraints: NoOverlap

## Execution
  python PerfectSquare.py -data=<datafile.json>

## Links
  - https://hal.science/hal-01245074
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  recreational, mzn21
"""

from pycsp3 import *

def ref_model(param_dict):
    size = param_dict["size"]
    squares = param_dict["squares"]
    nSquares = param_dict["nSquares"]


    # x[i] is the x-coordinate where is put the ith square
    x = VarArray(size=nSquares, dom=range(size + 1))

    # y[i] is the y-coordinate where is put the ith square
    y = VarArray(size=nSquares, dom=range(size + 1))

    satisfy(
        # unary constraints on x
        [x[i] + squares[i] <= size for i in range(nSquares)],

        # unary constraints on y
        [y[i] + squares[i] <= size for i in range(nSquares)],

        # no overlap on boxes
        NoOverlap(
            origins=[(x[i], y[i]) for i in range(nSquares)],
            lengths=[(w, w) for w in squares]
        )
    )
    #
    return x,y

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
    x,y = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
            y == dvar_dict["y"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

