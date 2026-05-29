"""
The Boolean Pythagorean triples problem is a problem from Ramsey theory about whether the positive integers can be colored red and blue
so that no Pythagorean triples consist of all red or all blue members.
The Boolean Pythagorean triples problem was solved by Marijn Heule, Oliver Kullmann and Victor W. Marek in May 2016 through a computer-assisted proof.
More specifically, the problem asks if it is possible to color each of the positive integers either red or blue, so that no triple of integers a, b, c,
satisfying a2 + b2 = c2 are all the same color.
For example, in the Pythagorean triple 3, 4 and 5 (32 + 42 = 52 ), if 3 and 4 are colored red, then 5 must be colored blue.

## Data
  A unique integer n

## Model
  constraints: NValues

## Execution
  python PythagoreanTriples.py -data=number

## Links
  - https://en.wikipedia.org/wiki/Boolean_Pythagorean_triples_problem
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
"""

from pycsp3 import *
from math import sqrt

n = data or 5

def ref_model(param_dict):
  n = param_dict['n']
  #
  RED, BLUE = 0, 1

  def conflicts():
      t = []
      for i in range(1, n + 1):
          i2 = i * i
          for j in range(i + 1, n + 1):
              j2 = j * j
              s = i2 + j2
              if s > n * n:
                  break
              sr = int(sqrt(s))
              if sr * sr == s:
                  t.append((i, j, sr))
      return t


  def valid_triple(i, j, k):
      if variant("table"):
          return (x[i], x[j], x[k]) in [(RED, RED, BLUE), (RED, BLUE, RED), (RED, BLUE, BLUE), (BLUE, RED, RED), (BLUE, RED, BLUE), (BLUE, BLUE, RED)]
      return NotAllEqual(x[i], x[j], x[k])


  # x[i] is RED (resp., BLUE) if integer i is in part/subset 0 (resp., 1)
  x = VarArray(size=n + 1, dom={RED, BLUE})

  satisfy(
      ## @symmetry-breaking removed
      # # putting 0 in the first setting an arbitrary value to integer 0  tag(symmetry-breaking)
      # x[0] == 0,

      # ensuring that each Pythagorean triple is valid
      [valid_triple(i, j, k) for i, j, k in conflicts()]
  )
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
    x = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")