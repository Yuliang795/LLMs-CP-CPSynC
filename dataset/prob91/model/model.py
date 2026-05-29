"""
Betty, Chris, Donald, Fred, Gary, Mary, and Paul want to align in one row for taking a photo.
Some of them have preferences next to whom they want to stand:
 - Betty wants to stand next to Gary and Mary.
 - Chris wants to stand next to Betty and Gary.
 - Fred wants to stand next to Mary and Donald.
 - Paul wants to stand next to Fred and Donald.

## Data
  all integrated (single problem)

## Model
  constraints: AllDifferent, Sum, Table

## Execution
  python Photo.py
  python Photo.py -variant=aux

## Tags
  single
"""

from pycsp3 import *

def ref_model(param_dict=None):

    # friends[i] is the position (in a row) of the ith friend
    betty, chris, donald, fred, gary, mary, paul = friends = VarArray(size=7, dom=range(7))

    preferences = [(betty, gary), (betty, mary), (chris, betty), (chris, gary), (fred, mary), (fred, donald), (paul, fred), (paul, donald)]

    # costs[i] is the cost of not respecting the ith preference
    costs = VarArray(size=len(preferences), dom={0, 1})

    T = {(i, j, 0 if abs(i - j) == 1 else 1) for i in range(7) for j in range(7) if i != j}

    satisfy(
        # all friends are at a different position
        AllDifferent(friends),

        # determining which preferences are not satisfied
        [(f1, f2, costs[i]) in T for i, (f1, f2) in enumerate(preferences)]
    )

    minimize(
        # minimizing the overall dissatisfaction
        Sum(costs)
    )
    #
    return friends, costs




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
    friends, costs = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            (friends[i] == dvar_dict["friends"][i] for i in range(7)),
            # friends == dvar_dict["friends"],
            Sum(costs) == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(costs) < dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(values(costs))} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")


