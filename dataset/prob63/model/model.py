"""
The goal of the asymmetric travelling purchaser problem is to decide where to buy each of a set of products,
and in which order to visit the purchase locations, in order to minimize the total travel and purchase costs.
Travel costs are asymmetric, and cities are laid out on a grid with travel only allowed between horizontally and vertically adjacent cities.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012/2016 Minizinc challenges.
The MZN model was proposed by Kathryn Francis.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  3-3-30-1.json

## Model
  constraints: Circuit, Element

## Execution
  python TPP.py -data=<datafile.json>
  python TPP.py -data=<datafile.dzn> -parser=TPP_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  realistic, mzn12, mzn16
"""

from pycsp3 import *

# _data = {
#   "nProducts": 30,
#   "distances": [
#     [0, 9, -1, 6, -1, -1, -1, -1, -1],
#     [8, 0, 15, -1, 14, -1, -1, -1, -1],
#     [-1, 5, 0, -1, -1, 15, -1, -1, -1],
#     [7, -1, -1, 0, 9, -1, 19, -1, -1],
#     [-1, 10, -1, 14, 0, 4, -1, 18, -1],
#     [-1, -1, 3, -1, 15, 0, -1, -1, 13],
#     [-1, -1, -1, 3, -1, -1, 0, 17, -1],
#     [-1, -1, -1, -1, 10, -1, 17, 0, 13],
#     [-1, -1, -1, -1, -1, 11, -1, 20, 0]
#   ],
#   "prices": [
#     [15, 20, 19, 14, 18, 3, 6, 15, 1, 7, 4, 16, 10, 1, 16, 15, 16, 1, 18, 18, 18, 13, 1, 9, 1, 18, 13, 14, 17, 16],
#     [17, 6, 19, 10, 5, 5, 1, 12, 7, 4, 19, 17, 9, 15, 6, 9, 20, 17, 16, 19, 3, 8, 13, 12, 2, 18, 9, 3, 2, 9],
#     [6, 10, 20, 16, 20, 11, 18, 7, 15, 1, 14, 6, 2, 2, 17, 11, 15, 13, 15, 16, 15, 5, 9, 4, 4, 8, 8, 1, 12, 14],
#     [18, 7, 18, 6, 11, 10, 9, 4, 11, 17, 17, 17, 2, 20, 15, 20, 9, 12, 11, 6, 16, 17, 5, 12, 17, 17, 9, 9, 12, 3],
#     [4, 11, 20, 16, 13, 4, 15, 3, 4, 18, 2, 16, 18, 5, 8, 18, 10, 17, 18, 10, 4, 7, 12, 7, 9, 16, 18, 9, 3, 16],
#     [17, 11, 11, 10, 16, 9, 1, 1, 16, 7, 19, 8, 9, 10, 3, 20, 12, 1, 19, 14, 6, 13, 2, 16, 10, 7, 17, 8, 4, 19],
#     [3, 8, 13, 18, 19, 6, 15, 12, 17, 20, 9, 19, 4, 4, 15, 1, 15, 10, 10, 13, 1, 19, 11, 17, 12, 9, 7, 16, 11, 1],
#     [7, 20, 20, 9, 5, 7, 2, 20, 19, 10, 18, 9, 19, 3, 17, 8, 20, 12, 10, 19, 9, 5, 2, 3, 20, 6, 6, 15, 7, 11]
#   ]
# }
from pycsp3.tools.curser import convert_to_namedtuples

def ref_model(param_dict):
  nProducts = param_dict['n']
  distances = param_dict['distances']
  prices = param_dict['prices']
  # nProducts, distances, prices = _data.values()
  distances, prices = convert_to_namedtuples({"d":distances, "p":prices})
  #

  nCities, maxDistance, maxPrice = len(distances), max(max(row) for row in distances), max(max(row) for row in prices)

  # x[i] is the city that succeeds to the ith city
  x = VarArray(size=nCities, dom=range(nCities))

  # tc[i] is the travel cost from going to the ith city to the next one
  tc = VarArray(size=nCities, dom=range(maxDistance + 1))

  # pl[j] is the purchase location of the jth product
  pl = VarArray(size=nProducts, dom=range(nCities - 1))

  # pc[j] is the purchase cost of the jth product
  pc = VarArray(size=nProducts, dom=range(maxPrice + 1))

  satisfy(
      # computing travel costs
      [tc[i] == distances[i][x[i]] for i in range(nCities)],

      # the purchase cost depends on the chosen purchase city
      [pc[j] == prices[pl[j]][j] for j in range(nProducts)],

      # purchasing a product at a city is only possible if you visit that city
      [x[pl[j]] != pl[j] for j in range(nProducts)],

      # a circuit is expected
      Circuit(x),

      # the last city must be visited (we start here)
      x[nCities - 1] != nCities - 1
  )

  minimize(
      # minimizing the total cost
      Sum(tc) + Sum(pc)
  )
  return x, pl, tc, pc


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
    x, pl, tc, pc = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
            pl == dvar_dict["pl"],
            Sum(tc) + Sum(pc) == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(tc) + Sum(pc) < dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(values(tc)+values(pc))} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")
