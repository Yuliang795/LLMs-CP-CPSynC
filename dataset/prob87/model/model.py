"""
The travelling salesman problem (TSP) asks the following question: "Given a list of cities and the distances between each pair of cities,
what is the shortest possible route that visits each city exactly once and returns to the origin city?" (from wikipedia).

## Data Example
  10-20-0.json

## Model
  constraints: Sum, Table

## Execution
  python TravelingSalesman.py -data=<datafile.json>
  python TravelingSalesman.py -data=<datafile.json> -variant=table

## Links
  - https://en.wikipedia.org/wiki/Travelling_salesman_problem

## Tags
  recreational
"""

from pycsp3 import *
from pycsp3.tools.curser import convert_to_namedtuples


def ref_model(param_dict):
    distances = convert_to_namedtuples({"d":param_dict["distances"]}).d

    nCities = len(distances)

    # c[i] is the ith city of the tour
    c = VarArray(size=nCities, dom=range(nCities))

    # d[i] is the distance between the cities i and i+1 chosen in the tour
    d = VarArray(size=nCities, dom=distances)

    satisfy(
        # Visiting each city only once
        AllDifferent(c)
    )

    satisfy(
        # computing the distance between any two successive cities in the tour
        distances[c[i]][c[i + 1]] == d[i] for i in range(nCities)
    )

    minimize(
        # minimizing the travelled distance
        Sum(d)
    )
    #
    return c,d


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
    c,d = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            c == dvar_dict["c"],
            Sum(d) == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(d) < dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(values(d))} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")

""" Comments
1) Writing dom=distances is equivalent (and more compact) than writing dom={v for row in distances for v in row}

2) Index auto-adjustment is used with c[i+1] (equivalent to c[(i+1) % nCities)
"""