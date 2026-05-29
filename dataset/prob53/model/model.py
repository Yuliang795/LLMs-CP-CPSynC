"""
An n x n array  of the integers from 1 to n^2 such that the difference between any integer
and its neighbor (horizontally, vertically, or diagonally, without wrapping around)
is greater than or equal to some value k is called a (n,k)-talisman square.

## Example
  A solution for the (4,2)-talisman square:
  ```
      1  8 11 14
      4 16  5  2
     12  9 13 10
     15  6  3  7
  ```

## Data
  A pair (n,k).

## Model
  constraints: AllDifferent

## Execution
  python Talisman.py -data=[number,number]

## Links
  - https://mathworld.wolfram.com/TalismanSquare.html

## Tags
  academic
"""

from pycsp3 import *

# n, k = data or (4, 2)

def ref_model(param_dict):
  n, k = param_dict['n'], param_dict['k']
  #
  limit = (n * (n * n + 1)) // 2

  # x[i][j] is the value in the talisman square at row i and column j
  x = VarArray(size=[n, n], dom=range(1, n * n + 1))

  satisfy(
      # all values must be different
      AllDifferent(x),

      ## @prob-model mismatch: >k -> >=k
      # the distance between two neighbouring cells must be strictly greater than k
      [
          [abs(x[i][j] - x[i][j + 1]) >= k for i in range(n) for j in range(n - 1)],
          [abs(x[i][j] - x[i + 1][j]) >= k for j in range(n) for i in range(n - 1)],
          [abs(dgn[i] - dgn[i + 1]) >= k for dgn in diagonals_down(x) for i in range(len(dgn) - 1)],
          [abs(dgn[i] - dgn[i + 1]) >= k for dgn in diagonals_up(x) for i in range(len(dgn) - 1)]
      ],

      ## @symmetry-breaking removed
      # # tag(symmetry-breaking)
      # x[0][0] == 1
  )
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