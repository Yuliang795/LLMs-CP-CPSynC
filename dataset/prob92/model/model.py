"""
There is one four-digit whole number x, such that the last four digits of x^2
are in fact the original number x. What is it?

## Data
  all integrated (single problem)

## Execution
  python Square.py

## Links
 - http://en.wikibooks.org/wiki/Puzzles/Arithmetical_puzzles/Digits_of_the_Square

## Tags
  single
"""

from pycsp3 import *

def ref_model(param_dict):
    
  # x is the number we look for
  x = Var(range(1000, 10000))

  # d[i] is the ith digit of x
  d = VarArray(size=4, dom=range(10))

  satisfy(
      d * [1000, 100, 10, 1] == x,

      (x * x) % 10000 == x
  )
  #
  return x,d


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
    x,d = ref_model(param_dict)
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