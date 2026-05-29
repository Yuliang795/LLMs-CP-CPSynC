"""
Related papers:
 - Mathematical methods of organizing and planning production, L. V. Kantorovich, Management Science, 6(4):366–422, 1960
 - From High-Level Model to Branch-and-Price Solution in G12, J. Puchinger, P. Stuckey, M. Wallace, and S. Brand, CPAIOR 2008: 218-232

## Data Example
  small.json

## Model
  constraints: Lex, Sum

## Execution
  python Cutstock.py -data=<datafile.json>
  python Cutstock.py -data=<datafile.dzn> -parser=Cutstock_ParserZ.py

## Tags
  recreational, xcsp25
"""

from pycsp3 import *





# nPieces, pieceLength, items = data
# lengths, demands = zip(*items)
# nItems = len(data.items)
# nPieces, pieceLength = data_["N"], data_["L"]
# lengths, demands = data_["i_length"], data_["i_demand"]
# nItems = len(lengths)
# print(lengths, type(lengths))


def ref_model(param_dict):
  nPieces, pieceLength = param_dict['N'], param_dict['L']
  nItems = param_dict['nItems']
  lengths, demands = param_dict['i_length'], param_dict['i_demand']
  
  # p[i] is 1 iff the ith piece of the stock is used
  p = VarArray(size=nPieces, dom={0, 1})

  # r[i][j] is the number of items of type j built using stock piece i
  r = VarArray(size=[nPieces, nItems], dom=lambda i, j: range(max(demands) + 1))

  satisfy(
      # not exceeding possible demands
      [r[i][j] <= demands[j] for i in range(nPieces) for j in range(nItems)],

      # each item demand must be exactly satisfied
      [Sum(r[:, j]) == demand for j, demand in enumerate(demands)],

      # each piece of the stock cannot provide more than its length
      [r[i] * lengths <= p[i] * pieceLength for i in range(nPieces)],

      ## @symmetry-breaking removed
      # # tag(symmetry-breaking)
      # [
      #     Decreasing(p),
      #     LexDecreasing(r)  # to be removed for MiniCOP track
      # ]
  )

  minimize(
      # minimizing the number of used pieces
      Sum(p)
  )
  #
  return r, p


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
    r,p = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            r == dvar_dict["r"],
            p == dvar_dict["p"],
            Sum(p) == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(p) < dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(values(p))} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")
