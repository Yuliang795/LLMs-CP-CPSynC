"""
Cardinality-constrained Multi-cycle Problem (CCMCP).

This problem appears as one of the main optimization problems modelling kidney exchange.
The problem consists of the prize-collecting assignment problem and an addition constraint stipulating that each subtour in the graph
has a maximum length K.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
The MZN model was proposed by Edward Lam and Vicky Mak-Hau.
No Licence was explicitly mentioned (MIT Licence is assumed).


## Data Example
  3-20-025-2.json

## Model
  constraints: AllDifferent, BinPacking, Precedence, Sum

## Execution
  python KidneyExchange.py -data=<datafile.json>
  python KidneyExchange.py -data=<datafile.dzn> -parser=KidneyExchange_ParserZ.py
  python KidneyExchange.py -data=<datafile.txt> -parser=KidneyExchange_ParserW.py

## Links
  - https://en.wikipedia.org/wiki/Optimal_kidney_exchange
  - https://www.preflib.org/dataset/00036
  - https://link.springer.com/article/10.1007/s10878-015-9932-4
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, notebook, mzn19, mzn23
"""

from pycsp3 import *
# _data = {
#   "weights": [
#     [0, -1, -1, -1, -1, -1, -1, 37, -1, 11, -1, -1, -1, 53, -1, -1, -1, -1, -1, -1],
#     [-1, 0, 57, 23, -1, 1, -1, 23, -1, -1, 19, -1, -1, -1, 2, 29, -1, -1, -1, -1],
#     [-1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 42, -1, -1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, 0, -1, -1, -1, 58, 39, 47, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, 18, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
#     [-1, 89, -1, 58, -1, 0, -1, -1, -1, -1, -1, -1, -1, 92, -1, 71, 56, -1, -1, 60],
#     [-1, -1, 35, -1, -1, -1, 0, 5, -1, -1, -1, 87, 61, 95, 63, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1, -1, 0, 57, -1, -1, -1, 67, 91, 70, 100, -1, -1, -1, -1],
#     [-1, -1, -1, 62, 94, 21, -1, 63, 0, -1, 45, 72, -1, -1, -1, -1, -1, -1, -1, -1],
#     [10, -1, -1, -1, -1, -1, 77, 44, 93, 0, 43, 10, -1, -1, -1, -1, -1, -1, -1, 57],
#     [-1, -1, 31, -1, 24, -1, -1, -1, -1, -1, 0, -1, -1, 41, 63, -1, -1, -1, 14, -1],
#     [13, -1, -1, 56, -1, 100, -1, -1, -1, 44, -1, 0, -1, 79, -1, -1, 23, -1, -1, 46],
#     [49, 80, -1, -1, -1, -1, -1, -1, 65, -1, -1, -1, 0, -1, -1, 37, -1, -1, 51, -1],
#     [-1, -1, -1, -1, -1, 94, -1, 29, -1, 23, -1, -1, 63, 0, -1, 4, -1, -1, -1, -1],
#     [-1, -1, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 94, 0, 2, -1, -1, 6, 21],
#     [-1, -1, -1, -1, -1, 61, -1, -1, 57, -1, -1, -1, -1, -1, -1, 0, -1, 71, -1, -1],
#     [21, 13, -1, 84, -1, -1, 34, -1, 97, 35, 3, 97, -1, -1, -1, -1, 0, 84, -1, 100],
#     [-1, -1, -1, -1, -1, -1, -1, 19, 16, -1, -1, 40, -1, -1, -1, -1, 61, 0, -1, -1],
#     [61, 82, 8, 2, -1, 25, -1, -1, 53, -1, -1, -1, 9, -1, -1, 31, -1, -1, 0, -1],
#     [-1, -1, 27, -1, -1, -1, -1, -1, 36, -1, -1, -1, 10, -1, -1, -1, -1, -1, -1, 0]
#   ],
#   "k": 3
# }

from pycsp3.tools.curser import convert_to_namedtuples

# weights, k = _data.values()
def ref_model(param_dict):
  weights = param_dict["weights"]
  k = param_dict["k"]
  weights = convert_to_namedtuples({"w":weights}).w
  #
  n = len(weights)

  # x[i] is the successor node of node i (in the cycle where i belongs)
  x = VarArray(size=n, dom=range(n))

  # y[i] is the cycle (index) where the node i belongs
  y = VarArray(size=n, dom=range(n))

  satisfy(
      AllDifferent(x),

      # ensuring correct cycles
      [y[i] == y[x[i]] for i in range(n)],

      # disabling infeasible arcs
      [x[i] != j for i in range(n) for j in range(n) if i != j and weights[i][j] < 0],

      # each cycle has k as maximum length
      BinPacking(y, sizes=1) <= k,

      ## @symmetry-breaking removed
      # # tag(symmetry-breaking)
      # Precedence(y)
  )

  maximize(
      # maximizing the sum of arc weights of selected cycles
      Sum(weights[i][x[i]] for i in range(n))
  )
  return x,y, weights


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
    x, y, weights = ref_model(param_dict)
    n = len(weights)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
            Sum(weights[i][x[i]] for i in range(n)) == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(weights[i][x[i]] for i in range(n)) > dvar_dict["z"]
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(weights[i][values(x)[i]] for i in range(n))} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")