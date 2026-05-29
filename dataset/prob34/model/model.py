"""
From Tony Hurlimann, A coin puzzle, SVOR-contest 2007.

## Data
  Two integers n and c

## Model
  constraints: Sum

## Execution
  python CoinsGrid.py -data=[number,number]

## Links
  - https://link.springer.com/book/10.1007/978-3-319-25883-6
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  academic, recreational, xcsp22
"""

from pycsp3 import *

# n, c = data or (8, 4)

def  ref_model(param_dict):
  n= param_dict['n']
  c= param_dict['c']
  # x[i][j] is 1 if a coin is placed at row i and column j
  x = VarArray(size=[n, n], dom={0, 1})
  z = Var(dom=range(n * n * (n - 1) ** 2 + 1)) 

  satisfy(
      # ensuring each row sums to c
      [Sum(x[i]) == c for i in range(n)],

      # ensuring each column sums to c
      [Sum(x[:, j]) == c for j in range(n)],

      # obj
      z == Sum(
            x[i][j] * abs(i - j) ** 2 for i in range(n) for j in range(n)
        )
  )

  minimize(
      z
  )
  return x, z

""" Comments
1) There are other variants in Hurlimann's paper (TODO)
2) Some data: (8,4) (8,5) (9,4) (10,4) (31,14)
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
    x, z = ref_model(param_dict)
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
        satisfy(
            LexIncreasing(z, dvar_dict["z"], strict=True)
            )
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{value(z)} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")