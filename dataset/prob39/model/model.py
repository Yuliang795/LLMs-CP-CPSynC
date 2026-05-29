"""
Generalized Peaceable Queens.

On a board, put the maximal number of black and white queens while having no attack from opposing sides.
The number of black queens must be equal to the number of white queens.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Hendrik 'Henk' Bierlee, under the MIT Licence.

## Data
  two integers (n,q)

## Model
  constraints: Cardinality, Lex, Precedence, Regular

## Execution
  python GeneralizedPeacableQueens.py -data=[number,number]

## Links
  - https://oeis.org/A250000
  - https://link.springer.com/chapter/10.1007/978-3-540-24664-0_19
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  academic, mzn22
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry

# n, q = 4,2#data  # the order (number of rows and columns) of the board and the number of armies
def ref_model(param_dict):
  n = param_dict['n']
  q = param_dict['q']
  #
  colors = range(q + 1)  # including 0

  symmetries = [f.apply_on(n) for f in TypeSquareSymmetry]


  def automaton():
      qs = Automaton.states_for(colors)
      trs = [(qs[0], 0, qs[0])] + [(qs[0], v, qs[v]) for v in range(1, q + 1)] + [(qs[v], [0, v], qs[v]) for v in range(1, q + 1)]
      return Automaton(start=qs[0], final=qs, transitions=trs)


  A = automaton()  # the automaton used to impose that queens are at peace

  # x[i][j] is the color is in the cell at row i and column j (0 if no queen)
  x = VarArray(size=[n, n], dom=colors)

  # z[i] is the number of queens for the ith color (excluding 0)
  z = VarArray(size=q, dom=range(n * n // q))

  satisfy(
      # at peace on every row
      [x[i] in A for i in range(n)],

      # at peace on every column
      [x[:, j] in A for j in range(n)],

      # at peace on all down-right diagonals (except corners)
      [[x[i][j] for i in range(n) for j in range(n) if i + j == k] in A for k in range(1, 2 * n - 2)],

      # at peace on all up-right diagonals (except corners)
      [[x[i][j] for i in range(n) for j in range(n) if i - j == k] in A for k in range(-n + 2, n - 1)],

      # counting the number of queens of each color
      Cardinality(
          within=x,
          occurrences={i: z[i - 1] for i in range(1, q + 1)}
      ),

      # ensuring the same number of queens of each color
      AllEqual(z),

      ## @symmetry-breaking removed
      # # tag(symmetry-breaking)
      # Precedence(
      #     within=x,
      #     values=range(1, q + 1)
      # ),

      # # tag(symmetry-breaking)
      # [x <= x[symmetry] for symmetry in symmetries]
  )

  maximize(
      # maximizing the number of queens on the board
      z[0]
  )
  #
  return x, z

"""
1) Data used in 2022 are:  (8,3), (9,5), (11,5), (13,5), (25,4)
2) Note that:
 x[symmetry]
   is a shortcut for
 [x[row] for row in symmetry]
   which, itself, is a shortcut for:
 [[x[k][l] for k, l in row] for row in symmetry]
3) Note that:
 [x <= x[symmetry] for symmetry in symmetries]
   is equivalent to:
 [LexIncreasing(x, x[symmetry]) for symmetry in symmetries]  
"""

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
            [x[i][j] == dvar_dict["x"][i][j] for i in range(len(x)) for j in range(len(x))],
            z == dvar_dict["z"]
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            # Since the number of queens is the same for each color, compare the first one is enough
            z[0] > dvar_dict["z"][0]
            )
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT | ref:{values(z)} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")