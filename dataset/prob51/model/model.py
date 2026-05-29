"""
From WikiPedia: "A Steiner system with parameters t, k, n, written S(t,k,n), is an n-element set S
together with a set of k-element subsets of S (called blocks) with the property
that each t-element subset of S is contained in exactly one block.
In an alternate notation for block designs, an S(t,k,n) would be a t-(n,k,1) design."

## Data
  Three integers (t,k,n)

## Model
  constraints: Count, Lex, Sum

## Execution
  python SteinerSystems -data=[number,number,number]

## Links
  - https://en.wikipedia.org/wiki/Steiner_system
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  academic, mzn21
"""

from pycsp3 import *
from math import comb

# t, k, n = 2,3,7#data
def ref_model(param_dict):
  t, k, n = param_dict['t'], param_dict['k'], param_dict['n']
  #
  m = comb(n, t) // comb(k, t)  # the number of blocks

  # x[i][p] is the pth value of the ith block
  x = VarArray(size=[m, k], dom=range(n))

  # b[i][v] is 1 if the value v is present in the ith block
  b = VarArray(size=[m, n], dom={0, 1})

  satisfy(
      ## @symmetry-breaking removed
      # # tag(symmetry-breaking)
      # [
      #     [Increasing(x[i], strict=True) for i in range(m)],
      #     LexIncreasing(x, strict=True)
      # ],

      # @@fix: each block must be a k-element subset
      [AllDifferent(x[i]) for i in range(m)],

      # computing the presence of values in blocks
      [b[i][v] == ExactlyOne(x[i][p] == v for p in range(k)) for i in range(m) for v in range(n)],

      # avoiding two similar t-elements
      [
          Sum(
              both(
                  b[i][v],
                  b[i][v] == b[j][v]
              ) for v in range(n)
          ) < t for i, j in combinations(m, 2)
      ]
  )
  return x

""" Comments
1) Data used in MZN21 are: (2,7,21) (3,3,11) (3,4,8) (4,4,10) (6,6,7)
2) The model used in Minizinc challenge 2021 involves set variables
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