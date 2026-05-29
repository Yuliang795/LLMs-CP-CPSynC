"""
An OPD (v,b,r) problem is to find a binary matrix of v rows and b columns such that:
   - each row sums to r,
   - the dot product between any pair of distinct rows is minimal

## Data
  Three integers (v,b,r)

## Model
  constraints: Lex, Maximum, Sum

## Execution
  python OPD.py -data=[number,number,number]
  python OPD.py -data=[number,number,number] -variant=aux

## Links
  - https://www.csplib.org/Problems/prob065/
  - https://link.springer.com/article/10.1007/s10601-006-9014-4
  - https://www.sciencedirect.com/science/article/abs/pii/S1571065314000596?via%3Dihub
  - https://link.springer.com/chapter/10.1007/11564751_7
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  academic, csplib
"""

from pycsp3 import *

def ref_model(param_dict):
    v, b, r = param_dict['v'], param_dict['b'], param_dict['r']

    # x[i][j] is the value at row i and column j
    x = VarArray(size=[v, b], dom={0, 1})

    satisfy(
        # each row sums to 'r'
        Sum(x[i]) == r for i in range(v)
    )

    minimize(
        # minimizing the maximum value of dot products between all pairs of distinct rows
        Maximum(x[i] * x[j] for i, j in combinations(v, 2))
    )

    ## @symmetric-breaking removed
    # satisfy(
    #     # tag(symmetry-breaking)
    #     LexIncreasing(x, matrix=True)
    # )
    #
    return x, v, b, r



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
    x, v, b, r = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
            # friends == dvar_dict["friends"],
            Maximum(x[i] * x[j] for i, j in combinations(v, 2)) == dvar_dict["lambda_val"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Maximum(x[i] * x[j] for i, j in combinations(v, 2)) < dvar_dict["lambda_val"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{max(values(x)[i] * values(x)[j] for i, j in combinations(v, 2))} - sol:{dvar_dict['lambda_val']}")
        else:
            print("opt@OPT")
