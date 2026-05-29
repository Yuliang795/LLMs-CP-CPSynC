"""
The Dreadsbury Mansion Mystery.

Someone who lives in Dreadsbury Mansion killed Aunt Agatha.
Agatha, the butler, and Charles live in Dreadsbury Mansion, and are the only people who live therein.
We know that:
 - A killer always hates his victim, and is never richer than his victim.
 - Charles hates no one that Aunt Agatha hates.
 - Agatha hates everyone except the butler.
 - The butler hates everyone not richer than Aunt Agatha.
 - The butler hates everyone Agatha hates.
 - No one hates everyone.

## Data
  all integrated (single problem)

## Model
  constraints: Count, Element

## Execution
  python Agatha.py

## Links
  - https://www.researchgate.net/publication/220531947_Seventy-Five_Problems_for_Testing_Automatic_Theorem_Provers

## Tags
  single
"""

from pycsp3 import *

def ref_model(param_dict):
    persons = agatha, butler, charles = 0, 1, 2

    # killer is the person who kills Agatha
    killer = Var(dom=persons)

    # hating[i][j] is 1 iff person i hates person j
    hating = VarArray(size=[3, 3], dom={0, 1})

    # richer[i][j] is 1 iff person i is richer than person j
    richer = VarArray(size=[3, 3], dom={0, 1})

    satisfy(
        # a killer always hates his victim
        hating[killer][agatha] == 1,

        # a killer is never richer than his victim
        richer[killer][agatha] == 0,

        # Charles hates no one that Agatha hates
        [
            If(
                hating[agatha][p],
                Then=~hating[charles][p]
            ) for p in persons
        ],

        # Agatha hates everybody except the butler
        [hating[agatha][p] == 1 for p in persons if p != butler],

        # the butler hates everyone not richer than Aunt Agatha
        [
            If(
                ~richer[p][agatha],
                Then=hating[butler][p]
            ) for p in persons
        ],

        # the butler hates everyone Agatha hates
        [
            If(
                hating[agatha][p],
                Then=hating[butler][p]
            ) for p in persons
        ],

        # no one hates everyone
        [
            Count(
                within=hating[p],
                value=0
            ) > 0 for p in persons
        ]
    )
    #
    return killer, hating, richer


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
    killer, hating, richer = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            killer == dvar_dict["killer"],
            hating == dvar_dict["hating"],
            richer == dvar_dict["richer"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")


""" Comments
1) it is possible to write hating[charles][p] == 0 instead of ~hating[charles][p]
2) it is possible to write Exist(hating[p], value=0) instead of Count(hating[p], value=0) > 0 
"""