"""
The Abbot's Puzzle, from "Amusements in Mathematics, Dudeney" (number 110).

We know that 100 bushels of corn were distributed among 100 people.
Each man received three bushels, each woman two, and each child half a bushel.
There are five times as many women as men.
How many men, women, and children were there?

## Data
  all integrated (single problem)

## Execution
  python Abbots.py

## Links
 - https://www.comp.nus.edu.sg/~henz/projects/puzzles/arith/index.html

## Tags
  single
"""

from pycsp3 import *

def ref_model(param_dict):
  # m is the number of men
  m = Var(range(100))

  # w is the number of women
  w = Var(range(100))

  # m is the number of children
  c = Var(range(100))

  satisfy(
      m + w + c == 100,
      m * 6 + w * 4 + c == 200,
      m * 5 == w
  )
  #
  return m,w,c


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
    m,w,c = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            m == dvar_dict["m"],
            w == dvar_dict["w"],
            c == dvar_dict["c"]
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")