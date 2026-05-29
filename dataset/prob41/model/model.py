"""
This is [Problem 005](https://www.csplib.org/Problems/prob005/) at CSPLib.

These problems have many practical applications in communications and electrical engineering.
The objective is to construct a binary sequence length n that minimizes the autocorrelations between bits.
Each bit in the sequence takes the value +1 or -1.

## Data
  A number n, the length of the sequence.

## Model
  constraints: Sum

## Execution
  python LowAutocorrelation.py -data=number

## Tags
  academic, csplib
"""

from pycsp3 import *

def ref_model(param_dict):
  n = param_dict['n']
  #
  # x[i] is the ith value of the sequence to be built.
  x = VarArray(size=n, dom={-1, 1})

  # y[k][i] is the ith product value required to compute the kth auto-correlation
  y = VarArray(size=[n - 1, n - 1], dom=lambda k, i: {-1, 1} if i < n - k - 1 else None)

  # c[k] is the value of the kth auto-correlation
  c = VarArray(size=n - 1, dom=lambda k: range(-n + k + 1, n - k))

  satisfy(
      [y[k][i] == x[i] * x[i + k + 1] for k in range(n - 1) for i in range(n - k - 1)],

      [Sum(y[k]) == c[k] for k in range(n - 1)]
  )
  minimize(
      # minimizing the sum of the squares of the auto-correlation
      Sum(c[k] * c[k] for k in range(n - 1))
  )

  return x,y,c

""" Comments 
1) For the objective, c * c is possible, but parsers must be updated
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
    x,y,c = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
            Sum(c[k] * c[k] for k in range(param_dict['n'] - 1)) == dvar_dict["z"]
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(c[k] * c[k] for k in range(param_dict['n'] - 1)) < dvar_dict["z"]
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(values(c)[k]*values(c)[k] for k in range(param_dict['n'] - 1))} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")