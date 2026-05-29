"""
In combinatorial mathematics, a superpermutation on n symbols is a string that contains each permutation of n symbols
as a substring. While trivial superpermutations can simply be made up of every permutation listed together,
superpermutations can also be shorter (except for the trivial case of n = 1) because overlap is allowed.
For instance, in the case of n = 2, the superpermutation 1221 contains all possible permutations (12 and 21),
but the shorter string 121 also contains both permutations.

It has been shown that for 1 ≤ n ≤ 5, the smallest superpermutation on n symbols has length 1! + 2! + ... + n!.
The first four smallest superpermutations have respective lengths 1, 3, 9, and 33, forming the strings 1, 121,
123121321, and 123412314231243121342132413214321.
However, for n = 5, there are several smallest superpermutations having the length 153.

## Data
  An integer n

## Model
  constraints: AllDifferent, Cardinality, Table

## Execution
  python Superpermutation.py -data=number
  python Superpermutation.py -data=number -variant=table

## Links
  - https://en.wikipedia.org/wiki/Superpermutation
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  academic, xcsp22
"""

from math import factorial
from itertools import permutations as it_permutations

from pycsp3 import *

n = 3#data
def ref_model(param_dict):
  n = param_dict['n']
  #
  m = sum(factorial(i) for i in range(1, n + 1))  # the length of the sequence; this is valid for 2 <= n <= 5 (see above)
  assert 2 <= n <= 5, "for the moment, the model is valid for n between 2 and 5"

  permutations = list(it_permutations(v for v in range(1, n + 1)))
  nPermutations = len(permutations)

  # x[i] is the ith value of the sequence
  x = VarArray(size=m, dom=range(1, n + 1))

  if not variant():

      # p[j] is the index in the sequence of the first value of the jth permutation
      p = VarArray(size=nPermutations, dom=range(m))

      satisfy(
          # all permutations start at different indexes  tag(redundant)
          AllDifferent(p),

          # ensuring that each permutation occurs in the sequence
          [x[p[j] + k] == permutations[j][k] for k in range(n) for j in range(nPermutations)]
      )
  return x, p

## @variant removed

## @symmetry-breaking removed
## @palindrom removed as not required in the problem description
# satisfy(
#     # setting the first permutation  tag(symmetry-breaking)
#     [x[i] == i + 1 for i in range(n)],

#     # constraining a palindrome  tag(palindrome)
#     [x[i] == x[-1 - i] for i in range(m // 2)]
# )



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
    x, p = ref_model(param_dict)
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