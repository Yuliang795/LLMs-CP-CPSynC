"""
Four friends are two women named Debra and Janet, and two men named Hugh and Rick.
They found that each of them is allergic to something different: eggs, mold, nuts and ragweed.
We would like to match each one's surname (Baxter, Lemon, Malone and Fleet) with his or her allergy.
We know that:
 - Rick is not allergic to mold
 - Baxter is allergic to eggs
 - Hugh is neither surnamed Lemon nor Fleet
 - Debra is allergic to ragweed
 - Janet (who isn't Lemon) is neither allergic to eggs nor to mold

## Data
  all integrated (single problem)

## Model
  constraints: AllDifferent

## Execution
  python Allergy.py

## Tags
  single
"""

from pycsp3 import *

def ref_model(param_dict=None):
  friends = Debra, Janet, Hugh, Rick = "Debra", "Janet", "Hugh", "Rick"

  # foods[i] is the friend allergic to the ith food
  eggs, mold, nuts, ragweed = foods = VarArray(size=4, dom=friends)

  # surnames[i] is the friend with the ith surname
  baxter, lemon, malone, fleet = surnames = VarArray(size=4, dom=friends)

  satisfy(
      AllDifferent(foods),
      AllDifferent(surnames),

      mold != Rick,
      eggs == baxter,
      lemon != Hugh,
      fleet != Hugh,
      ragweed == Debra,
      lemon != Janet,
      eggs != Janet,
      mold != Janet
  )
  #
  return foods, surnames


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
    foods, surnames = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            (foods[i] == dvar_dict["foods"][i] for i in range(4)),
            (surnames[i] == dvar_dict["surnames"][i] for i in range(4)),
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")