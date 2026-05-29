"""
The change-making problem addresses the question of finding the minimum number of coins (of certain denominations) that
add up to a given amount of money. It is a special case of the integer knapsack problem, and has applications wider than
just currency.
It is also the most common variation of the coin change problem, a general case of partition in which, given the
available denominations of an infinite set of coins, the objective is to find out the number of possible ways
of making a change for a specific amount of money, without considering the order of the coins.

### Example
  For n=13, one needs at least 4 coins:
  ``` 13 = 3x1 + 10```

## Data
  a number n, the given amount of money

## Model
  There are two variants: a main one and a compact one (with fewer variables).

  constraints: Sum

## Execution
  python ChangeMaking.py -data=number
  python ChangeMaking.py -data=number -variant=compact

## Links
  - https://en.wikipedia.org/wiki/Change-making_problem

## Tags
  academic
"""

from pycsp3 import *

# def ref_model(param_dict):
#   k = param_dict['n'] # default value if not provided
#   # if not variant():
#   # c1 is the number of coins of 1 cent
#   c1 = Var(range(50))

#   # c5 is the number of coins of 5 cents
#   c5 = Var(range(50))

#   # c10 is the number of coins of 10 cents
#   c10 = Var(range(50))

#   # c20 is the number of coins of 20 cents
#   c20 = Var(range(50))

#   # c50 is the number of coins of 50 cents
#   c50 = Var(range(50))

#   # e1 is the number of coins of 1 euro
#   e1 = Var(range(50))

#   # e2 is the number of coins of 2 euros
#   e2 = Var(range(50))

#   satisfy(
#       # the given change must be correct
#       [c1, c5, c10, c20, c50, e1, e2] * [1, 5, 10, 20, 50, 100, 200] == k
#   )

#   minimize(
#       # the given change must have the minimum number of coins
#       c1 + c5 + c10 + c20 + c50 + e1 + e2
#   )
#   return [c1, c5, c10, c20, c50, e1, e2]
  

  # elif variant("compact"):
  #     # coins[i] is the number of coins of the ith type
  #     coins = VarArray(size=7, dom=range(50))

  #     satisfy(
  #         # the given change must be correct
  #         coins * [1, 5, 10, 20, 50, 100, 200] == k
  #     )

  #     minimize(
  #         # the given change must have the minimum number of coins
  #         Sum(coins)
  #     )


def ref_model(param_dict):
    k = param_dict["n"]
    denominations = param_dict["denominations"]   # e.g. [1, 2, 5, 10]

    # x[i] = number of coins using value denominations[i]
    coins = VarArray(
        size=len(denominations),
        dom=range(k // min(denominations) + 1)
    )

    satisfy(
        coins * denominations == k
    )

    minimize(
        Sum(coins)
    )

    return coins
    

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
    coins = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            [coins[i] == dvar_dict["coins"][i] for i in range(len(coins))],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum(coins) < sum(dvar_dict['coins']),
            )
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum(values(coins))} - sol:{sum(dvar_dict['coins'])}")
        else:
            print("opt@OPT")