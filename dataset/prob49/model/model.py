"""
The goal is to put m queens in a chess board such that none of the queens can attack each other, and to put n knights such that
all knights form a cycle. Note that the size of the board si n.

## Data
  A pair (n,m) where n is the size of the chess board and n the number of queens.

## Model
  constraints: AllDifferent

## Execution
  python QueensKnights.py -data=[number,number]

## Links
  - https://dblp.org/rec/conf/ecai/BoussemartHLS04.html

## Tags
  academic
"""

from pycsp3 import *

n, nKnights = (5, 4)  # n is the order(board width), and so the number of queens

def ref_model(param_dict):
  n, nKnights = param_dict['n'], param_dict['m']
  # q[i] is the column number of the board where is put the ith queen (in the ith row)
  q = VarArray(size=n, dom=range(n))

  # k[i] is the cell number of the board where is put the ith knight
  k = VarArray(size=nKnights, dom=range(n * n))

  satisfy(
      # all queens are put in different columns
      AllDifferent(q),

      # controlling no two queens on the same upward diagonal
      AllDifferent(q[i] + i for i in range(n)),

      # controlling no two queens on the same downward diagonal
      AllDifferent(q[i] - i for i in range(n)),

      # all knights are put in different cells
      AllDifferent(k),

      # all knights form a cycle
      [(abs(k[i] // n - k[i + 1] // n), abs(k[i] % n - k[i + 1] % n)) in {(1, 2), (2, 1)} for i in range(nKnights)]
  )
  return q, k

""" Comments
0) Index auto-adjustment is active: k[i + 1] is the same as k[(i + 1) % nKnights]
1) Adding  (q[i] != k[j] % n) | (i != k[j] // n) for i in range(n) for j in range(nKnights) does not seem to filter more values.
2) Expressing a table constraint where the scope does not list simple variables entails automatically introducing auxiliary variables at compilation time
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
    q,k = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            q == dvar_dict["q"],
            k == dvar_dict["k"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")