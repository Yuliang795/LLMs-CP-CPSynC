"""
The Traveling Salesman Problem with Time Windows (TSPTW) is a popular variant of the TSP where the salesman’s customers
must be visited within given time windows.
See IJCAI paper below.

## Data Example
  n020w020-1.json

## Model
  constraints: AllDifferent, Element, Sum

## Execution
  python TSP_TW1.py -data=<datafile.json>
  python TSP_TW1.py -data=<datafile.txt> -parser=TSP_TW_Parser.py

## Links
  - https://www.ijcai.org/proceedings/2022/0659.pdf
  - https://github.com/xgillard/ijcai_22_DDLNS
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
"""

from pycsp3 import *

from pycsp3.tools.curser import convert_to_namedtuples

def ref_model(param_dict):
  distances = param_dict["distances"]
  windows = param_dict["windows"]
  #
  distances = convert_to_namedtuples({"d":distances}).d
  #

  Earliest, Latest = cp_array(zip(*windows))
  horizon = max(Latest) + 1
  n = len(distances)

  # x[i] is the customer (node) visited in the ith position
  x = VarArray(size=n + 1, dom=range(n))

  # a[i] is the time when is visited the customer in the ith position
  a = VarArray(size=n, dom=range(horizon))

  satisfy(
      #  making it a tour while starting and ending at city 0
      [
          x[0] == 0,
          x[-1] == 0,
          a[0] == 0
      ],

      AllDifferent(x[:-1]),

      # enforcing time windows
      [
          [Earliest[x[i]] <= a[x[i]] for i in range(n)],
          [a[x[i]] <= Latest[x[i]] for i in range(n)],
          [a[x[i + 1]] >= a[x[i]] + distances[x[i], x[i + 1]] for i in range(n - 1)]
      ]
  )

  # z = Var(dom=range(99999))
  # satisfy(
  #     z == Sum(distances[x[i], x[(i + 1) % n]] for i in range(n))
  # )
  minimize(
      # minimizing travelled distance
      Sum(distances[x[i], x[(i + 1) % n]] for i in range(n))
  )
  return x, a, distances


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
    x, a, distances = ref_model(param_dict)
    n = len(a)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
            a == dvar_dict["a"],
            Sum(distances[x[i], x[(i + 1) % n]] for i in range(n)) == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(distances[x[i], x[(i + 1) % n]] for i in range(n)) < dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(distances[values(x)[i], values(x)[(i + 1) % n]] for i in range(n))} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")


