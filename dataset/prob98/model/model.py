"""
PyCSP3 Model (see pycsp.org)

Data can come:
 - either directly from a JSON file
 - or from an intermediate parser

Example:
  python Rack.py -data=Rack_r2.json
"""

from pycsp3 import *

def ref_model(param_dict=None):
    nRacks, models, cardTypes = param_dict["nRacks"], param_dict["models"], param_dict["cardTypes"]
    models.append([0, 0, 0])  # we add first a dummy model (0,0,0)
    powers, sizes, costs = zip(*models)
    cardPowers, cardDemands = zip(*cardTypes)
    nModels, nTypes = len(models), len(cardTypes)

    table = {(i, powers[i], sizes[i], costs[i]) for i in range(nModels)}

    # m[i] is the model used for the ith rack
    m = VarArray(size=nRacks, dom=range(nModels))

    # p[i] is the power of the model used for the ith rack
    p = VarArray(size=nRacks, dom=powers)

    # s[i] is the size (number of connectors) of the model used for the ith rack
    s = VarArray(size=nRacks, dom=sizes)

    # c[i] is the cost (price) of the model used for the ith rack
    c = VarArray(size=nRacks, dom=costs)

    # nc[i][j] is the number of cards of type j put in the ith rack
    nc = VarArray(size=[nRacks, nTypes], dom=lambda i, j: range(min(max(sizes), cardDemands[j]) + 1))

    satisfy(
        # linking rack models with powers, sizes and costs
        [(m[i], p[i], s[i], c[i]) in table for i in range(nRacks)],

        # connector-capacity constraints
        [Sum(nc[i]) <= s[i] for i in range(nRacks)],

        # power-capacity constraints
        [nc[i] * cardPowers <= p[i] for i in range(nRacks)],

        # demand constraints
        [Sum(nc[:, j]) == cardDemands[j] for j in range(nTypes)],

        ## @symmetry-breaking removed
        # # tag(symmetry-breaking)
        # [Decreasing(m), imply(m[0] == m[1], nc[0][0] >= nc[1][0])]
    )

    minimize(
        # minimizing the total cost being paid for all racks
        Sum(c)
    )
    #
    return m, nc, c

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
    m, nc, c = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            m == dvar_dict["m"],
            nc == dvar_dict["nc"],
            Sum(c) == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(c) < dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(values(c))} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")
