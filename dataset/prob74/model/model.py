"""
You are given a grid of size n × m containing numbers being parts of dominoes.
For example, for n = 7 and m = 8, the grid contains all dominoes from 0-0 to 6-6.
One has to find the position (and rotation) of each domino.

# Data Example
  grid01.json

## Model
  constraints: AllDifferent, Table

## Execution
  python Dominoes.py -data=<datafile.json>
  python Dominoes.py -data=<datafile.json> -variant=table

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-24662-6_11
  - https://www.researchgate.net/publication/266585191_Dominoes_as_a_Constraint_Problem
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  recreational, xcsp23
"""

from pycsp3 import *
from pycsp3.tools.curser import convert_to_namedtuples


def ref_model(param_dict):
  grid = convert_to_namedtuples({"g":param_dict['grid']}).g
  # grid = data
  nRows, nCols, nValues = len(grid), len(grid[0]), len(grid)
  dominoes = [(i, j) for i in range(nValues) for j in range(i, nValues)]  # pairs of values to be considered
  indexes = range(nRows * nCols)  # indexes of cells

  P = [[i * nCols + j for i in range(nRows) for j in range(nCols) if grid[i][j] == value] for value in range(nValues)]  # possible positions

  # x[i][j] is the index (position) in the grid of the value i of the domino i-j
  x = VarArray(size=[nValues, nValues], dom=lambda i, j: indexes if i <= j else None)

  # y[i][j] is the index (position) in the grid of the value j of the domino i-j
  y = VarArray(size=[nValues, nValues], dom=lambda i, j: indexes if i <= j else None)

  satisfy(
      # each part of each domino in a different cell
      AllDifferent(x + y),

      # unary constraints
      [
          (
              x[i][j] in P[i],
              y[i][j] in P[j]
          ) for i, j in dominoes
      ],
  )

  satisfy(
      # adjacency constraints
      If(
          d != nCols,  # if not adjacent in the same column
          Then=both(  # then adjacent in the same line
              d == 1,
              x[i][j] // nCols == y[i][j] // nCols
          )
      ) for i, j in dominoes if (d := abs(x[i][j] - y[i][j]),)
  )
  #
  return x,y


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
    # print(dvar_dict)
    #
    x,y = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
            y == dvar_dict["y"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")





""" Comments

1) One could use the If structure as follows:
   If(
      abs(x[i][j] - y[i][j]) != nCols,  # if not adjacent values in the same column
      Then=(abs(x[i][j] - y[i][j]) == 1) & (x[i][j] // nCols == y[i][j] // nCols)  # then adjacent values in the same line
   ) for i, j in dominoes

"""