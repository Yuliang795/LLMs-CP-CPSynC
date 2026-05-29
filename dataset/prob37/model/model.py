"""
A costas array is a pattern of n marks on an n∗n grid, one mark per row and one per column,
in which the n∗(n−1)/2 vectors between the marks are all-different.

See problem 076 at CSPLib.

## Data
  A unique integer, the order of the grid

## Model
  constraints: AllDifferent

## Execution
  python CostasArray.py -data=number

## Links
  - https://en.wikipedia.org/wiki/Costas_array
  - https://www.csplib.org/Problems/prob076/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  academic, csplib, xcsp22
"""

from pycsp3 import *

def ref_model(param_dict):
  n = param_dict['n']

  # x[i] is the row where is put the ith mark (on the ith column)
  x = VarArray(size=n, dom=range(n))

  satisfy(
      # all marks are on different rows (and columns)
      AllDifferent(x),

      # all displacement vectors between the marks must be different
      [
          AllDifferent(
              x[i] - x[i + d] for i in range(n - d)
          ) for d in range(1, n - 1)
      ]
  )
  return x,n
""" Comments
1) How to break all symmetries?  x[0] <= math.ceil(n / 2), x[0] < x[-1], ... ? TODO
"""


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

    # prepare decision variables
    x,n = ref_model(param_dict)
    x_sol = dvar_dict["x"]
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            [x[i] == x_sol[i] for i in range(n)],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

