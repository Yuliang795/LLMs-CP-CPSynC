"""
On a square grid of size n × n, all numbers ranging from 1 to n*n must be put so that the numbers surrounding each number add to a multiple of that number.

## Data
  A unique integer n

## Model
  constraints: AllDifferent, Sum

## Execution
  python AnotherMagicSquare.py -data=number

## Links
  - http://benvitale-funwithnum3ers.blogspot.com/2010/12/another-kind-of-magic-square.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
"""

from pycsp3 import *

def ref_model(param_dict):
  n = param_dict['n']

  # x[i][j] is the value at row i and column j
  x = VarArray(size=[n, n], dom=range(1, n * n + 1))

  satisfy(
      AllDifferent(x),

      # ensuring that the numbers surrounding a number v add to a multiple of v
      [Sum(x.around(i, j)) % x[i][j] == 0 for i in range(n) for j in range(n)]
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
1) There are 0, 8 and 0 solutions for n = 2, 3 and 4
2) For being compatible with the competition mini-track, we use:
   # y[i,j] is the multiple used for the cell at row i and column j
   y = VarArray(size=[n, n], dom=range(1, 8*(n * n) + 1))

   # ensuring that the numbers surrounding a number v add to a multiple of v
   [Sum(x.around(i, j)) == x[i][j] * y[i][j] for i in range(n) for j in range(n)]
"""