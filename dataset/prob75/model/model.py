"""
Given an edge-weighted directed graph with possibly many cycles, the task is to find an acyclic sub-graph of maximal weight.

## Data Example
  example.json

## Model
  constraints: AllDifferent, Sum

## Execution
  python GraphMaxAcyclic.py -data=<datafile.json>
  python GraphMaxAcyclic.py -data=<datafile.json> -variant=cnt
  python GraphMaxAcyclic.py -data=<datafile.txt> -dataparser=GraphMaxAcyclic_Parser.py

## Tags
  recreational
"""

from pycsp3 import *

def ref_model(param_dict):
    n = param_dict['nNodes']
    arcs = param_dict['arcs']
    #
    # n, arcs = data

    valid_arcs = [(i, j) for i in range(n) for j in range(n) if i != j and arcs[i][j] != 0]
    valid_numbers = [len([(i, j) for i in range(n) if (i, j) in valid_arcs]) for j in range(n)]

    # x[i] is the number associated with the ith node; arcs are only possible from greater to lower numbers (nodes)
    x = VarArray(size=n, dom=range(n))

    # a[i][j] is 1 iff the arc from i to j is selected
    a = VarArray(size=[n, n], dom=lambda i, j: {0, 1} if (i, j) in valid_arcs else None)

    satisfy(
        # different numbers must be associated to nodes
        AllDifferent(x)
    )

    
    satisfy(
        # ensuring acyclicity
        a[i][j] == (x[i] > x[j]) for (i, j) in valid_arcs
    )


    maximize(
        # maximising the summed weight of selected arcs
        Sum(a[i][j] * arcs[i][j] for (i, j) in valid_arcs)
    )
    #
    return x, a, arcs, valid_arcs


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
    x, a, arcs, valid_arcs = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            a == dvar_dict["a"],
            Sum(a[i][j] * arcs[i][j] for (i, j) in valid_arcs) == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(a[i][j] * arcs[i][j] for (i, j) in valid_arcs) > dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(values(a)[i][j] * arcs[i][j] for (i, j) in valid_arcs)} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")







""" Comments

1) A possible variant "smart ?
   elif variant("smart"):
      # c[i][j] is the cost of the link between i and j (whatever the direction)
      c = varArray(size=[n, n], dom=lambda i, j: {arcs[i][j], arcs[j][i]}, when=lambda i, j: (arcs[i][j] != 0 or arcs[j][i] != 0) and i < j)
      ... TODO
"""