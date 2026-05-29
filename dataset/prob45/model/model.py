"""
A Latin square of order n is an n by n array filled with n different symbols (for example, values between 1 and n),
each occurring exactly once in each row and exactly once in each column.
Two latin squares of the same order n are orthogonal if each pair of elements in the same position occurs exactly once.
The most easy way to see this is by concatenating elements in the same position and verify that no pair appears twice.
There are orthogonal latin squares of any size except 1, 2, and 6.

## Data
  a unique integer, the order of the problem instance

## Example
  A solution for n=5:
  ```
    [0, 1, 2, 3, 4]          [0, 1, 2, 3, 4]
    [4, 2, 3, 0, 1]          [3, 4, 1, 2, 0]
    [3, 4, 1, 2, 0]          [4, 2, 3, 0, 1]
    [1, 3, 0, 4, 2]          [2, 0, 4, 1, 3]
    [2, 0, 4, 1, 3]          [1, 3, 0, 4, 2]
  ```

## Model
  constraints: AllDifferent, Table

## Execution
  python Ortholatin.py -data=number

## Links
  - https://en.wikipedia.org/wiki/Mutually_orthogonal_Latin_squares
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  academic, xcsp22
"""

from pycsp3 import *

# n = data or 5

def ref_model(param_dict):
  n = param_dict['n']
  # x is the first Latin square
  x = VarArray(size=[n, n], dom=range(n))

  # y is the second Latin square
  y = VarArray(size=[n, n], dom=range(n))

  # z is the matrix used to control orthogonality
  z = VarArray(size=[n * n], dom=range(n * n))

  T = {(i, j, i * n + j) for i in range(n) for j in range(n)}

  satisfy(
      # ensuring that x is a Latin square
      AllDifferent(x, matrix=True),

      # ensuring that y is a Latin square
      AllDifferent(y, matrix=True),
      ## @unspecified constraint removed
      # # ensuring that values on diagonals are different  tag(diagonals)
      # [AllDifferent(dgn) for dgn in [diagonal_down(x), diagonal_up(x), diagonal_down(y), diagonal_up(y)]],

      # ensuring orthogonality of x and y through z
      AllDifferent(z),

      # computing z from x and y
      [(x[i][j], y[i][j], z[i * n + j]) in T for i in range(n) for j in range(n)],

      ## @symmetry-breaking is removed
      # # tag(symmetry-breaking)
      # [
      #     (
      #         x[0][j] == j,
      #         y[0][j] == j
      #     ) for j in range(n)
      # ]
  )
  return x, y

""" Comments
1) Note that a less compact way of posting symmetry_breaking constraints is:
 # tag(symmetry-breaking)
 [[x[0][j] == j for j in range(n)], [y[0][j] == j for j in range(n)]],
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
    x, y = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x== dvar_dict["x"],
            y== dvar_dict["y"],
            # [x[i][j] == dvar_dict["x"][i][j] for i in range(len(x[0])) for j in range(len(x[0]))],
            # [y[i][j] == dvar_dict["y"][i][j] for i in range(len(y[0])) for j in range(len(y[0]))],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")