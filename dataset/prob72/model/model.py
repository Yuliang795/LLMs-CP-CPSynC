"""
The purpose of the game is to fill a grid of size n × n with all values ranging from 1 to n*n such that:
  - if the next number in the sequence is going to be placed vertically or horizontally, then it must be placed exactly three squares away
  from the previous number (there must be a two square gap between the numbers);
  - if the next number in the sequence is going to be placed diagonally, then it must be placed exactly two squares away
  from the previous number (there must be a one square gap between the numbers).

## Data
  A unique integer n

## Model
  constraints: AllDifferent, Count, Table

## Execution
  python CalvinPuzzle.py -data=number
  python CalvinPuzzle.py -data=number -variant=table

## Links
  - https://chycho.blogspot.com/2014/01/an-exercise-for-mind-10-by-10-math.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
"""

from pycsp3 import *

def ref_model(param_dict):
  n = param_dict['n']
  # n = data or 5

  # x[i][j] is the value in the grid at row i and column j
  x = VarArray(size=[n, n], dom=range(1, n * n + 1))

  # possible neighbours
  offsets = [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (-2, 2), (2, -2), (2, 2)]
  N = [[[x[i + oi][j + oj] for (oi, oj) in offsets if 0 <= i + oi < n and 0 <= j + oj < n] for j in range(n)] for i in range(n)]

  satisfy(
      # putting all values from 1 to n*n in the grid
      AllDifferent(x),

      ## @symmetry-breaking removed
      # tag(symmetry-breaking)
      # x[0][0] == 1
  )

  satisfy(
      # each cell must be linked to its neighbors
      If(
          x[i][j] < n * n,
          Then=Exist(y == x[i][j] + 1 for y in N[i][j])
      ) for i in range(n) for j in range(n)
  )
  #
  return x


""" Comments
1) Using an hybrid table is possible
2) 552 solutions for n=5 (with the symmetry-breaking constraint)
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