"""
## Data Example
  caterpillar13.json

## Model
  constraints: Maximum, Table

## Execution
  python CyclicBandwidth.py -data=<datafile.json>
  python CyclicBandwidth.py -data=<datafile.json> -variant=aux
  python CyclicBandwidth.py -data=<datafile.json> -variant=table
  python CyclicBandwidth.py -data=<datafile.txt> -parser=CyclicBandwith_Parser.py

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0305054814003177
  - https://www.tamps.cinvestav.mx/~ertello/cbmp.php
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, xcsp22
"""

from pycsp3 import *

# n, edges = data or (5, [[0, 1], (0, 4), (1, 2), (1, 3), (2, 3), (2, 4)])
# edges = [tuple(t) for t in edges]  # because from JSON, we get lists and not tuples (which may be a problem with some conditions)

def ref_model(param_dict):
    n = param_dict['n']
    edges = param_dict['edges']
    edges = [tuple(t) for t in edges]  # because from JSON, we get lists and not tuples (which may be a problem with some conditions)
    #
    # x[i] is the label of the ith node
    x = VarArray(size=n, dom=range(n))

    satisfy(
        AllDifferent(x)
    )

    if not variant():
        minimize(
            Maximum(min(abs(x[i] - x[j]), n - abs(x[i] - x[j])) for i, j in edges)
        )
    ## @variant removed
    #
    return x, edges, n

""" Comments
1) With an aggressive ub, optimality is proved:
  java ace CyclicBandwidth-path300.xml -ale=4 -ub=3
  java ace CyclicBandwidth-aux-path300.xml -ub=2
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
    x, edges, n = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
           
            Maximum(min(abs(x[i] - x[j]), n - abs(x[i] - x[j])) for i, j in edges) == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Maximum(min(abs(x[i] - x[j]), n - abs(x[i] - x[j])) for i, j in edges) < dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{max([min(abs(values(x)[i] - values(x)[j]), n - abs(values(x)[i] - values(x)[j])) for i, j in edges])} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")

