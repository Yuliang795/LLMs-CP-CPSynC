"""
Problem 081 on CSPLib

## Data Example
  example.json

## Model
 constraints: Channel, Slide, Table

## Execution:
  python Blackhole.py -data=<datafile.json>

## Links
 - https://www.csplib.org/Problems/prob081/

## Tags
  recreational, notebook, csplib
"""

from pycsp3 import *

def ref_model(param_dict=None):
    m = param_dict['nCardsPerSuit']
    piles = param_dict['piles']
    # m, piles = data  # m denotes the number of cards per suit
    nCards = 4 * m

    # x[i] is the value j of the card at the ith position of the built stack
    x = VarArray(size=nCards, dom=range(nCards))

    # y[j] is the position i of the card whose value is j
    y = VarArray(size=nCards, dom=range(nCards))

    T = {(i, j) for i in range(nCards) for j in range(nCards) if i % m == (j + 1) % m or j % m == (i + 1) % m}

    satisfy(
        # linking variables of x and y
        Channel(x, y),

        # the Ace of Spades is initially put on the stack
        y[0] == 0,

        # cards must be played in the order of the piles
        [Increasing(y[pile], strict=True) for pile in piles],

        # each new card put on the stack must be at a rank higher or lower than the previous one
        Slide((x[i], x[i + 1]) in T for i in range(nCards - 1))
    )
    #
    return x,y, m, piles


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
    x,y, m, piles = ref_model(param_dict)
    #
    nCards = 4 * m
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            (x[i] == dvar_dict["x"][i] for i in range(nCards)),
            (y[i] == dvar_dict["y"][i] for i in range(nCards)),
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

""" Comments
1) Slide is only used to have more compact XCSP3 instances
   we could have written: [(x[i], x[i + 1]) in table for i in range(nCards - 1)]  
2) Increasing(y[pile], strict=True)
 is equivalent to:
   Increasing([y[j] for j in pile], strict=True)
"""

