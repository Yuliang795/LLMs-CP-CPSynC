"""
Someone in the university ate Alice’s sandwich at the cafeteria. We want to find out who the culprit is.
The witnesses are unanimous about the following facts:
 - Three persons were in the cafeteria at the time of the crime: Alice, Bob, and Sascha.
 - The culprit likes Alice.
 - The culprit is taller than Alice.
 - Nobody is taller than himself.
 - If A is taller than B, then B is not taller than A.
 - Bob likes no one that Alice likes.
 - Alice likes everybody except Bob.
 - Sascha likes everyone that Alice likes.
 - Nobody likes everyone.

## Data
  all integrated (single problem)

## Model
  constraints: Count, Element

## Execution
  python Sandwich.py

## Tags
  single
"""

from pycsp3 import *

def ref_model(param_dict):
    alice, bob, sascha = persons = 0, 1, 2

    # culprit is among alice (0), bob (1) and sascha (2)
    culprit = Var(persons)

    # liking[i][j] is 1 iff the ith guy likes the jth guy
    liking = VarArray(size=[3, 3], dom={0, 1})

    # taller[i][j] is 1 iff the ith guy is taller than the jth guy
    taller = VarArray(size=[3, 3], dom={0, 1})

    satisfy(
        # the culprit likes Alice
        liking[culprit][alice] == 1,

        # the culprit is taller than Alice
        taller[culprit][alice] == 1,

        # nobody is taller than himself
        [taller[p][p] == 0 for p in persons],

        ## @problem description mismatch: the story does NOT require total comparability
        ##  the ith guy is taller than the jth guy iff the reverse is not true
        # [taller[p1][p2] != taller[p2][p1] for p1 in persons for p2 in persons if p1 != p2],
        ## Asymmetry only (no pair must be comparable)
        [taller[p1][p2] + taller[p2][p1] <= 1 for p1 in persons for p2 in persons if p1 != p2],

        # Bob likes no one that Alice likes
        [If(liking[alice][p], Then=~liking[bob][p]) for p in persons],

        # Alice likes everybody except Bob
        [liking[alice][p] == 1 for p in persons if p != bob],
        ## @prob description mismatch: added "Alice likes everybody except Bob"
        liking[alice][bob] == 0,

        # Sascha likes everyone that Alice likes
        [If(liking[alice][p], Then=liking[sascha][p]) for p in persons],

        # nobody likes everyone
        [Count(liking[p], value=0) >= 1 for p in persons]
    )
    #
    return culprit, liking, taller


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
    culprit, liking, taller = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            culprit == dvar_dict["culprit"],
            liking == dvar_dict["liking"],
            taller == dvar_dict["taller"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")