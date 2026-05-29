"""
The queens graph is a graph with n*n nodes corresponding to the squares of a chess-board.
There is an edge between nodes iff they are on the same row, column, or diagonal, i.e. if two queens on those squares would attack each other.
The coloring problem is to color the queens graph with n colors.
See paper cited below.

### Example
  An example of a solution for n=7 is:
  ```
     4 5 3 1 2 0 6
     0 6 4 5 3 1 2
     1 2 0 6 4 5 3
     5 3 1 2 0 6 4
     6 4 5 3 1 2 0
     2 0 6 4 5 3 1
     3 1 2 0 6 4 5
  ```

## Data
  A number n, the size of the chessboard

## Model
  constraints: AllDifferent

## Execution
  python ColouredQueens.py -data=number

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-30210-0_17

## Tags
  academic
"""

from pycsp3 import *

def  ref_model(param_dict):
  n= param_dict['n']
  # x[i][j] is the color at row i and column j
  x = VarArray(size=[n, n], dom=range(n))

  satisfy(
      # ensuring different colors on rows and columns
      AllDifferent(x, matrix=True),

      # ensuring different colors on downward diagonals
      [AllDifferent(dgn) for dgn in diagonals_down(x)],

      # ensuring different colors on upward diagonals
      [AllDifferent(dgn) for dgn in diagonals_up(x)]
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

    # verify optimality of the solution
    elif args.check == 'opt':
        raise NotImplementedError("No opt check for this CSP model.")