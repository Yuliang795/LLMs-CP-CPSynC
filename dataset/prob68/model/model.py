"""
An anti-magic square of order n is an arrangement of the numbers 1 to n*n in a square,
such that the sums of the n rows, the n columns and the two main diagonals form a sequence
of 2n + 2 consecutive integers.

## Data
  A unique integer n

## Model
  constraints: AllDifferent, Sum, Maximum, Minimum

## Execution
  python AntimagicSquare.py -data=number

## Links
  - https://en.wikipedia.org/wiki/Antimagic_square
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
"""

from pycsp3 import *

def ref_model(param_dict):
  n = param_dict['n']

  lb, ub = (n * (n + 1)) // 2, ((n * n) * (n * n + 1)) // 2

  # x[i][j] is the value put in the cell of the matrix at coordinates (i,j)
  x = VarArray(size=[n, n], dom=range(1, n * n + 1))

  # y[k] is the sum of values in the kth line (row, column or diagonal)
  y = VarArray(size=2 * n + 2, dom=range(lb, ub + 1))

  satisfy(
      # all values must be different
      AllDifferent(x),

      # computing sums
      [
          [y[i] == Sum(x[i]) for i in range(n)],
          [y[n + j] == Sum(x[:, j]) for j in range(n)],
          y[2 * n] == Sum(diagonal_down(x)),
          y[2 * n + 1] == Sum(diagonal_up(x))
      ],

      # all sums must be consecutive
      [
          AllDifferent(y),
          Maximum(y) - Minimum(y) == 2 * n + 1
      ],

      ## @symmetry-breaking removed
      # # tag(symmetry-breaking)
      # # ensuring Frenicle standard form
      # [
      #     x[0][0] < x[0][-1],
      #     x[0][0] < x[-1][0],
      #     x[0][0] < x[-1][-1],
      #     x[0][1] < x[1][0]
      # ]
  )
  #
  return x,y,n

""" Comments
1) It is possible to relax so as to have a COP.
    minimizing the expression: Maximum(x) - Minimum(y)  
2) For being compatible with the competition mini-track, we use:
  z = VarArray(size=2*n+2, dom=range(2*n+2))
  
  [y[z[i]] +1 == y[z[i+1]] for i in range(2*n+1)], 
"""

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
    x,y,n = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            # [x[i][j] == dvar_dict["x"][i][j] for i in range(n) for j in range(n)],
            x == dvar_dict["x"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")