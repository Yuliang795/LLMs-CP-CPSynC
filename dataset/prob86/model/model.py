"""
The Brussels Central Problem (Fom course at UCL -- Louvain La Neuve)

The SNCB finally decided to rely on optimization technologies to schedule the departure
of its fleet at Brussels central. The problem to be solved is the following:
- Each train has a scheduled departure time.
- If a train departs earlier or later than expected, a penalty cost is incurred per time unit.
- After a train has left the station, no other train can depart for a given period
 (number of time units, or 'gap', which depends upon the train that has left).
- The goal is to minimize the cost incurred by early and late departs.

## Data Example
  Brussels.json

## Model
  constraints: NoOverlap, Sum

## Execution
  python TrainSchedule.py -data=<datafile.json>

## Tags
  recreational
"""

from pycsp3 import *


def ref_model(param_dict):
    trains = param_dict["trains"]
    # trains = data or default_data("Brussels.json")
    departures, gaps, costs = zip(*trains)
    nTrains, horizon = len(trains), max(departures) + max(gaps) * 4 + 1  # arbitrary horizon

    # x[i] is the time at which leaves the ith train
    x = VarArray(size=nTrains, dom=range(horizon))

    ## aux obj
    z = Var(dom=range(horizon * max(costs) + 1))  # safe upper bound
    satisfy(
        z == Sum(abs(x[i] - departures[i]) * costs[i] for i in range(nTrains))
    )

    satisfy(
        # respecting security gaps between two trains leaving the station
        NoOverlap(
            origins=(x[i], x[j]),
            lengths=(gaps[i], gaps[j])
        ) for i, j in combinations(nTrains, 2)
    )

    minimize(
        # minimizing penalty costs
        # Sum(abs(x[i] - departures[i]) * costs[i] for i in range(nTrains))
        z
    )
    #
    return x,z


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
    x,z = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
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
1) we can also write:
 (s[i] + gaps[i] <= s[j]) | (s[j] + gaps[j] <= s[i]) for i, j in combinations(range(nTrains), 2)
  but the solver might not recognize the NoOverlap/disjunctive constraints
"""