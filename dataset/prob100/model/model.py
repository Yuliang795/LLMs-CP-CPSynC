"""
See Problem 086 on CSPLib, and VVRLib.

## Data Example
  A-n32-k5.json

## Model
  constraints: AllDifferent, Cardinality, Element, Sum

## Execution
  python CVRP.py -data=<datafile.json>

## Links
  - https://www.csplib.org/Problems/prob086/
  - http://vrp.galgos.inf.puc-rio.br/index.php/en/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, csplib, xcsp22
"""


from pycsp3 import *
from pycsp3.tools.curser import convert_to_namedtuples


def ref_model(param_dict):
  nVehicles, nNodes, capacity, demands, distances = param_dict.values()
  distances = convert_to_namedtuples({"d1":distances}).d1
  demands = convert_to_namedtuples({"d2":demands}).d2
  # nVehicles = nNodes // 4  # This is a kind of hard coding, which can be at least used for Set A (Augerat, 1995)

    ## @problem description mismatch
    # def max_tour():
    #     t = sorted(demands)
    #     i, s = 1, 0
    #     while i < nNodes and s < capacity:
    #         s += t[i]
    #         i += 1
    #     return i - 2
    # nSteps = max_tour()
  nSteps = (nNodes - 1)
  n0s = nVehicles * nSteps - nNodes + 1

  # c[i][j] is the jth customer (step) during the tour of the ith vehicle
  c = VarArray(size=[nVehicles, nSteps], dom=range(nNodes))

  # d[i][j] is the demand of the jth customer during the tour of the ith vehicle
  d = VarArray(size=[nVehicles, nSteps], dom=demands)

  satisfy(
      AllDifferent(c, excepting=0),

      # ensuring that all demands are satisfied
      Cardinality(
          within=c,
          occurrences={0: n0s} | {i: 1 for i in range(1, nNodes)}
      ),

      # no holes permitted during tours
      [
          If(
              c[i][j] == 0,
              Then=c[i][j + 1] == 0
          ) for i in range(nVehicles) for j in range(nSteps - 1)
      ],

      # computing the collected demands
      [demands[c[i][j]] == d[i][j] for i in range(nVehicles) for j in range(nSteps)],

      # not exceeding the capacity of each vehicle
      [Sum(d[i]) <= capacity for i in range(nVehicles)],

      ## @symmetry-breaking removed 
      # # tag(symmetry-breaking)
      # Decreasing(c[:, 0])
  )

  ## @aux obj
  obj = (
      Sum(distances[0][c[i][0]] for i in range(nVehicles))
      + Sum(distances[c[i][j]][c[i][j + 1]] for i in range(nVehicles) for j in range(nSteps - 1))
      + Sum(distances[c[i][-1]][0] for i in range(nVehicles))
  )
  # a safe (loose) upper bound for z
  max_dist = max(distances[i][j] for i in range(nNodes) for j in range(nNodes))
  U = max_dist * ((nNodes - 1) + nVehicles)
  z = Var(range(U + 1))
  satisfy(z == obj)
  minimize(z)

  # minimize(
  #     # minimizing the total traveled distance by vehicles
  #     Sum(distances[0][c[i][0]] for i in range(nVehicles))
  #     + Sum(distances[c[i][j]][c[i][j + 1]] for i in range(nVehicles) for j in range(nSteps - 1))
  #     + Sum(distances[c[i][-1]][0] for i in range(nVehicles))
  # )
  #
  return c,z,nVehicles,nSteps, d


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
    c,z,nVehicles,nSteps, d = ref_model(param_dict)
    #
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            [c[i][j] == dvar_dict["c"][i][j] for i in range(nVehicles) for j in range(nSteps)],
            z == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            z < dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{value(z)} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")


""" Comments
1) We can check the solution for the instance A-n32-k5 with:
 [c[2][k] == v for k, v in enumerate([21, 31, 19, 17, 13, 7, 26])],
 [c[4][k] == v for k, v in enumerate([12, 1, 16, 30])],
 [c[1][k] == v for k, v in enumerate([27, 24])],
 [c[0][k] == v for k, v in enumerate([29, 18, 8, 9, 22, 15, 10, 25, 5, 20])],
 [c[3][k] == v for k,v in enumerate([14, 28, 11, 4, 23, 3, 2, 6])]
 
2) The AllDifferent constraint is redundant
"""