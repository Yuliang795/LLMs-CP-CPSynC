"""
From the Oz Primer.

The code of Professor Smart's safe is a sequence of 9 distinct
nonzero digits d1 .. d9 such that the following equations and
inequations are satisfied:
```
       d4 - d6   =   d7
  d1 * d2 * d3   =   d8 + d9
  d2 + d3 + d6   <   d8
            d9   <   d8
  d1 <> 1, d2 <> 2, ..., d9 <> 9
```
Can you find the correct combination?

## Data
  all integrated (single problem)

## Model
  constraints: AllDifferent

## Execution
  python SafeCracking.py

## Links
 -  http://www.comp.nus.edu.sg/~henz/projects/puzzles/digits/index.html

## Tags
  single
"""

from pycsp3 import *

def ref_model(param_dict=None):
  # x[i] is the i(+1)th digit
  x = VarArray(size=9, dom=lambda i: {v for v in range(1, 10) if v != i + 1})

  satisfy(
      AllDifferent(x),
      x[3] - x[5] == x[6],
      x[0] * x[1] * x[2] == x[7] + x[8],
      x[1] + x[2] + x[5] < x[7],
      x[8] < x[7]
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