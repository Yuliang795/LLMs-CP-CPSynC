"""
This problem is taken from Daily Telegraph and Sunday Times.
The problem is to find, for an equilateral triangular grid of size n (length of a side),
the maximum number of nodes that can be selected without having all selected corners of any equilateral triangle
of any size or orientation.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015/2019/2022 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data
  An integer n

## Model
  constraints: Sum

## Execution
  python Triangular.py -data=number

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  academic, mzn15, mzn19, mzn22
"""

from pycsp3 import *

# n = 3#data
def ref_model(param_dict):
  n = param_dict['n']
  #
  # x[i][j] is 1 iff the jth node in the ith row is selected
  x = VarArray(size=[n, n], dom=lambda i, j: {0, 1} if i >= j else None)

  satisfy(
      # avoiding the three corners of any equilateral triangle to be selected
      Sum(
          x[i + m][j],
          x[i + k][j + m],
          x[i + k - m][j + k - m]
      ) <= 2 for i in range(n) for j in range(i + 1) for k in range(1, n - i) for m in range(k)
  )

  maximize(
      # maximizing the number of selected nodes
      Sum(x)
  )
  return x

""" Comments
1) Data used in Minizinc challenges are:
   10, 16, 22, 28, 37 in 2015
   10, 17, 23, 29, 37 in 2019
   10, 18, 24, 30, 39 in 2022
   09, 11, 14, 20, 31 in 2024
2)
  AtLeastOne(
        within=[x[i + m][j], x[i + k][j + m], x[i + k - m][j + k - m]],
        value=0
    ) for i in range(n) for j in range(i + 1) for k in range(1, n - i) for m in range(k)
  seems to be less efficient
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
            Sum(x) == dvar_dict["z"]
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(x) > dvar_dict["z"]
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum([sum([i for i in r if i !=None]) for r in values(x)])} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")