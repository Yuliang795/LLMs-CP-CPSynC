"""
This is [Problem 017](https://www.csplib.org/Problems/prob017/) at CSPLib.

The edges of a complete graph (with n nodes) must be coloured with the minimum number of colours.
There must be no monochromatic triangle in the graph, i.e. in any triangle at most two edges have the same colour.
With 3 colours, the problem has a solution if n < 17.

## Data
  A number n, the number of nodes of the graph.

## Model
  constraints: Maximum, NValues

## Execution
  python Ramsey.py -data=number

## Tags
  academic, csplib
"""

from pycsp3 import *

# n = data or 6

def ref_model(param_dict):
  n = param_dict['n']
  #
  # x[i][j] is the color of the edge between nodes i and j
  x = VarArray(size=[n, n], dom=lambda i, j: range((n * (n - 1)) // 2) if i < j else None)

  satisfy(
      # no monochromatic triangle in the graph
      NotAllEqual(x[i][j], x[i][k], x[j][k]) for (i, j, k) in combinations(n, 3)
  )

  minimize(
      Maximum(x)
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
            Maximum(x) == dvar_dict["z"]
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Maximum(x) < dvar_dict["z"]
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{max([max([i if i !=None else 0 for i in r]) for r in values(x)])} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")