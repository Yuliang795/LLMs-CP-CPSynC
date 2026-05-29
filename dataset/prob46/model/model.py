"""
This is [Problem 110](https://www.csplib.org/Problems/prob110/) at CSPLib.

In the “Armies of queens” problem, we are required to place two equal-sized armies of black and white queens on a chessboard
so that the white queens do not attack the black queens (and necessarily vice versa) and to find the maximum size of two such armies.

## Example
  The optimum for a chessboard of size 8 is 9.
  A possible solution is
  ```
    W . . W W W . .
    . . . . W W . .
    W . . . . . . .
    W . . W . . . .
    . . . . . . B .
    . . . . . . B B
    . B B . . . . B
    . B B . . . B .
  ```

## Data
  A number n, the size of the chessboard

## Model
  There are two variants "m1" and "m2"

  constraints: Count, Sum

## Execution
  python PeacableArmies.py -data=number -variant=m1
  python PeacableArmies.py -data=number -variant=m2

## Tags
  academic, csplib
"""

from pycsp3 import *

# n = data or 6


def queen_attack(i1, j1, i2, j2):
    return i1 == i2 or j1 == j2 or abs(i1 - i2) == abs(j1 - j2)  # same row, column or diagonal

def ref_model(param_dict):
  n = param_dict['n']
  #
  # b[i][j] is 1 if a black queen is in the cell at row i and column j
  b = VarArray(size=[n, n], dom={0, 1})

  # w[i][j] is 1 if a white queen is in the cell at row i and column j
  w = VarArray(size=[n, n], dom={0, 1})

  satisfy(
      # no two queens in the same cell
      [b[i][j] + w[i][j] <= 1 for i in range(n) for j in range(n)],

      # no two opponent queens can attack each other
      [
          (
              b[i1][j1] + w[i2][j2] <= 1,
              w[i1][j1] + b[i2][j2] <= 1
          ) for (i1, j1, i2, j2) in product(range(n), repeat=4) if (i1, j1) < (i2, j2) and queen_attack(i1, j1, i2, j2)
      ],

      # ensuring the same numbers of black and white queens
      Sum(b) == Sum(w)
  )

  maximize(
      # maximizing the number of black queens (and consequently, the size of the armies)
      Sum(b)
  )

  ## @variant removed
  return b, w

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
    b, w = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            b == dvar_dict["b"],
            w == dvar_dict["w"],
            Sum(b) == dvar_dict["army_size"]
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(b) > dvar_dict["army_size"]
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(sum(r) for r in values(b))} - sol:{dvar_dict['army_size']}")
        else:
            print("opt@OPT")