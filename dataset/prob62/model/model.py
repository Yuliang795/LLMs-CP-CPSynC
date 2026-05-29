"""
An open shop problem is identical to a job-shop problem with the exception that there is no ordering on the tasks of a job.
A job is a sequence of tasks.
A task involves processing by a single machine for some duration.
A machine can operate on at most one task at a time, for each job at most one task can be performed at a time.
Tasks cannot be interrupted.
The goal is to schedule each job to minimise the finishing time (makespan).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014 Minizinc challenge.
The MZN model was proposed by Diarmuid Grimes (adapted from Ralph Becket model).
Instances were taken from benchmarks proposed by Taillard, Gueret and Prin, and Brucker et al.; see links below.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  gp10-4.json

## Model
  constraints: Cumulative, NoOverlap

## Execution
  python OpenShop.py -data=<datafile.json>
  python OpenShop.py -data=<datafile.dzn> -parser=OpenShop_ParserZ.py

## Links
  - https://en.wikipedia.org/wiki/Open-shop_scheduling
  - https://www.sciencedirect.com/science/article/abs/pii/037722179390182M
  - https://link.springer.com/article/10.1023/A:1018930613891
  - https://www.sciencedirect.com/science/article/pii/S0166218X96001163
  - https://www.minizinc.org/challenge2014/results2014.html

## Tags
  realistic, mzn14
"""

from pycsp3 import *


def ref_model(param_dict):
  nMachines = param_dict['m']
  durations = param_dict['durations']
  # nMachines, durations = _data.values()
  #
  nJobs = len(durations)
  Time = range(sum(sum(row) for row in durations) + 1)

  # x[i][j] is the starting time of the ith job on the jth machine (task)
  x = VarArray(size=[nJobs, nMachines], dom=Time)

  # z is the make-span
  z = Var(dom=Time)

  satisfy(
      # tasks on the same job cannot overlap
      [
          NoOverlap(
              origins=(x[i][j1], x[i][j2]),
              lengths=(durations[i][j1], durations[i][j2])
          ) for i in range(nJobs) for j1, j2 in combinations(nMachines, 2)
      ],

      # tasks on the same machine cannot overlap
      [
          NoOverlap(
              origins=(x[i1][k], x[i2][k]),
              lengths=(durations[i1][k], durations[i2][k])
          ) for i1, i2 in combinations(nJobs, 2) for k in range(nMachines)
      ],

      # tasks on the same job cannot overlap
      [
          Cumulative(
              tasks=[Task(origin=x[i][j], length=durations[i][j], height=1) for j in range(nMachines)]
          ) <= 1 for i in range(nJobs)
      ],

      # tasks on the same machine cannot overlap
      [
          Cumulative(
              tasks=[Task(origin=x[i][j], length=durations[i][j], height=1) for i in range(nJobs)]
          ) <= 1 for j in range(nMachines)
      ],

      # the finishing time must be no earlier than the finishing time of any task
      [x[i][j] + durations[i][j] <= z for i in range(nJobs) for j in range(nMachines)]
  )

  minimize(
      z
  )
  return x, z




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
    x, z = ref_model(param_dict)
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

