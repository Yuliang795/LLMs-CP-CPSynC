"""
Problem 063 on CSPLib.

There is a bunch of people bidding for things. A bid has a value, and the bid is for a set of items. If we have two bids, call them A and B,
and there is an intersection on the items they bid for, then we can accept bid A or bid B, but we cannot accept both of them.
However, if A and B are bids on disjoint sets of items then these two bids are compatible with each other, and we might accept both.
The problem then is to accept compatible bids such that we maximise the sum of the values of those bids (i.e. make most money).

## Data
  example.json

## Model
  constraints: Count, Sum

## Command Line
  python Auction.py [-solve]
  python Auction.py -data=<datafile.json>

## Links
 - https://www.csplib.org/Problems/prob063/

## Tags
  realistic, csplib
"""

from pycsp3 import *

# bids = data or default_data("example.json")
# bids = [
#     {"value": "10", "items": [1, 2]},
#     {"value": "20", "items": [1, 3]},
#     {"value": "30", "items": [2, 4]},
#     {"value": "40", "items": [2, 3, 4]},
#     {"value": "14", "items": [1]}
#   ]

def ref_model(param_dict):
  bid_values=param_dict['bid_values']
  bid_items=param_dict['bid_items']
  bids = [
      {"value": str(bid_values[i]), "items": bid_items[i]}
      for i in range(len(bid_values))
  ]
  #
  items = sorted({item for bid in bids for item in bid['items']})
  vals = integer_scaling(bid['value'] for bid in bids)
  nBids = len(bids)

  # x[i] is 1 iff the ith bid is selected
  x = VarArray(size=nBids, dom={0, 1})

  satisfy(
      # avoiding intersection of bids
      Count(within=scp, value=1) <= 1 for item in items if (scp := [x[i] for i, bid in enumerate(bids) if item in bid['items']],)
  )

  maximize(
      # maximizing summed values of selected bids
      x * vals
  )
  return x

"""
1) we avoid using values instead of vals as name for the list of bid values 
   as it may enter in conflict with the function values() in a notebook 
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
            Sum(x * param_dict['bid_values']) == dvar_dict["z"]
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(x * param_dict['bid_values']) > dvar_dict["z"]
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum([j*param_dict['bid_values'][i] for i,j in enumerate(values(x))])} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")