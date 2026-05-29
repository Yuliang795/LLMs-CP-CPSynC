"""
Little Problem given by Audrey at n-Side (see problem in OscaR).

Based on a little game I used to play in high school when I was getting bored in the classroom...
Draw a ten cells by ten cells board.
The purpose is to fill in all cells with numbers from 0 to 99.
You start by writing 0 in whatever cell.
From there on, you need to write the 1 by moving around in one of the following ways:
  - Move by 3 cells horizontally or vertically
  - Or move by 2 cells diagonally
Then, starting from the 1, you need to write the 2 using the same permitted moves, and so on.

The problem can be generalized for any order n.

## Data
  An integer n, the number of cells

## Model
  constraints: Circuit

## Execution
  python Audrey.py -data=number
  python Audrey.py -data=number -variant=display1
  python Audrey.py -data=number -variant=display2

## Tags
  academic, recreational
"""


## The puzzle as described is asking for the grid of visitation orders (because the user fills in 0, 1, 2 … in the cells).


from pycsp3 import *


def ref_model(param_dict):
  # n = data or 10
  n=param_dict['n']
  n2 = n * n

  def reachable(i, j):
      possible_cells = [(i - 3, j), (i + 3, j), (i, j - 3), (i, j + 3), (i - 2, j - 2), (i - 2, j + 2), (i + 2, j - 2), (i + 2, j + 2)]
      return {k * n + l for k, l in possible_cells if 0 <= k < n and 0 <= l < n}



  #* x[i] = j means: from cell i, the next visited cell is j.
  # x[i] is the index of the cell of the board following the ith cell in the circuit
  x = VarArray(size=n2, dom=lambda i: reachable(i // n, i % n))

  satisfy(
      # ensuring that we build a circuit
      Circuit(x)
  )
  #
  return x




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
    x= ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            # [x[i][j] == dvar_dict["x"][i][j] for i in range(n) for j in range(n)],
            x == dvar_dict["x"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")



""" Comments
1) The main model variant is sufficient to compute solutions.
   It is the fastest model. Hence, in a complex-world application, 
   adding constraints for pure presentational issue should be carefully thought.    
2) The variant 'display1' allows us to display the values (and not only the chaining).
   From this variant, to really get a matrix being printed, on can add:
     b = VarArray(size=[n, n], dom=range(n2))
     satisfy(
       b[i // n][i % n] == y[i] for i in range(n2)
     )     
3) The variant 'display2' allows us to directly print the values in a matrix.
   This involves a constraint 'ElementMatrix' whose computed value must be equal to a variable.    
4) We obtain 96 solutions for n=5 with the three variants.
"""