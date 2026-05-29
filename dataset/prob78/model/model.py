"""
PyCSP3 Model (see pycsp.org)

Data can come:
 - either directly from a JSON file
 - or from an intermediate parser

Example:
  python Knapsack.py -data=Knapsack_20-50-00.json
"""

from pycsp3 import *
from pycsp3.tools.curser import convert_to_namedtuples

# capacity, items = data
# item_weights, item_values = zip(*items)

# capacity=50
# item_weights = [1, 5, 2, 12, 12, 6, 12, 10, 4, 3, 6, 6, 6, 11, 12, 9, 5, 4, 6, 9]
# item_values = [44, 89, 25, 48, 53, 61, 4, 83, 93, 24, 46, 46, 38, 88, 3, 63, 26, 54, 39, 36]


def ref_model(param_dict):
    capacity=param_dict['capacity']
    nItems = param_dict['nItems']
    item_weights = convert_to_namedtuples({"w":param_dict['item_weights']}).w
    item_values = convert_to_namedtuples({"v":param_dict['item_values']}).v

    # x[i] is 1 iff the ith item is selected
    x = VarArray(size=nItems, dom={0, 1})

    satisfy(
        # not exceeding the capacity of the knapsack
        x * item_weights <= capacity
    )

    maximize(
        # maximizing summed up value (benefit)
        x * item_values
    )
    #
    return x,nItems,item_values


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
    x,nItems,item_values = ref_model(param_dict)
    #
    print(dvar_dict, item_values)
    #
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

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            x * item_values > dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum([values(x)[i]*item_values[i] for i in range(nItems)])} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")
