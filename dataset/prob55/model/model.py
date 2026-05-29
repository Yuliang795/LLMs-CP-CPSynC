"""
There are n countries.
Each pair of two countries is either at war or has a peace treaty.
Each pair of two countries that has a common enemy has a peace treaty.
What is the minimum number of peace treaties?

The minimum number of peace treaties for n in [2..12] seems to be floor(n^2/4), see https://oeis.org/A002620
Hence, it is 0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 36, 42, 49, 56, 64, 72, 81, ...

## Data
  an integer n

## Model
  constraints: Sum

## Execution
  python WarOrPeace.py -data=number
  python WarOrPeace.py -data=number -variant=or

## Links
  - https://oeis.org/A002620
  - http://www.hakank.org/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  academic, xcsp22
"""

from pycsp3 import *

# n = 4
def ref_model(param_dict):
  n = param_dict['n']
  #
  WAR, PEACE = 0, 1

  # x[i][j] is 1 iff countries i and j have a peace treaty
  x = VarArray(size=[n, n], dom=lambda i, j: {WAR, PEACE} if i < j else None)

  if not variant():
      satisfy(
          If(
              x[i][j] != PEACE,
              Then=NotExist(
                  both(
                      x[min(i, k)][max(i, k)] == WAR,
                      x[min(j, k)][max(j, k)] == WAR
                  ) for k in range(n) if different_values(i, j, k)
              )
          ) for i, j in combinations(n, 2)
      )

  ## @variant removed

  minimize(
      # minimizing the number of peace treaties
      Sum(x)
  )
  return x

""" Comments
1) The model variant 'or' seems to be far more efficient
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
            Sum(x) < dvar_dict["z"]
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum([sum([i for i in r if i !=None]) for r in values(x)])} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")