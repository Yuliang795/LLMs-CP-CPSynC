"""
From the IBM Challenge "Ponder This".

There are people living in the separate squares of a rectangular grid.
Each resident's neighbours are those who live in the squares that have a common edge with that resident's square.
Each resident of the grid is assigned a natural number k in the range 1..5
with the condition that the numbers 1, 2, ..., k-1 are present in the squares of his/her neighbors.
Find a configuration (assignment of numbers) of all neighbours, so that the sum of their numbers are maximised.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The original MZN model was proposed by Peter J. Stuckey, with a Licence that sems to be like a MIT Licence.

## Data
  two integers (n,m)

## Model
  There are two variants:
    - a main one with intensional constraints,
    - a 'table' variant with extensional constraints

  Constraints: Count, Lex, Sum, Table

## Execution
  python Neighbours.py -data=[number,number]

## Links
  - https://research.ibm.com/haifa/ponderthis/challenges/December2012.html
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  academic, mzn18, mzn21
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry, TypeRectangleSymmetry

# n, m = 3,3#data  # number of rows and number of columns

def ref_model(param_dict):
    n = param_dict['n']
    m = param_dict['m']
    #
    symmetries = [sym.apply_on(n) for sym in TypeSquareSymmetry] if n == m else [sym.apply_on(n, m) for sym in TypeRectangleSymmetry]


    def domain_x(i, j):
        if i in {0, n - 1} and j in {0, m - 1}:  # the four corners
            return range(1, 4)
        if i in {0, n - 1} or j in {0, m - 1}:  # the extreme lines or columns (border of the rectangle) without corners
            return range(1, 5)
        return range(1, 6)


    # x[i][j] is the value in the grid at coordinates (i,j)
    x = VarArray(size=[n, m], dom=domain_x)

    if not variant():
        satisfy(
            # ensuring valid neighbours
            If(
                x[i][j] >= k,
                Then=Exist(x.beside(i, j), value=k - 1)
            ) for i in range(n) for j in range(m) for k in range(2, 6)
        )

    ## @variant removed
    ## @symmetry-breaking removed
    # satisfy(
    #     # tag(symmetry-breaking)
    #     x <= x[symmetry] for symmetry in symmetries
    # )

    maximize(
        Sum(x)
    )
    return x

""" Comments
1) Data used in challenges are:
 2018: (5,5), (4,7), (7,8), (6,6), (9,4)
 2021: (9,14), (40,50), (20,19), (4,4), (4,9)
2) Note that:
 Exist(y == k - 1 for y in x.beside(i, j))
  is an alternative to:
 Exist(x.beside(i, j), value= k - 1)
3) Note that:
 x <= x[symmetry]
is equivalent to:
 LexIncreasing(x, x[symmetry]) 

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
    x = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
            Sum(x) == dvar_dict["z"]
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(x) > dvar_dict["z"]
            )
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(sum(row) for row in values(x))} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")