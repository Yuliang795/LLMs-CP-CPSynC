"""
This models a routing problem based on a little example of Mario's day.
Mario is an Italian Plumber and his work is mainly to find gold in the plumbing of all the houses of the neighborhood.
Mario is moving in the city using his kart that has a specified amount of fuel.
Mario starts his day of work from his house and always ends to his friend Luigi's house to have the supper.
The problem here is to plan the best path for Mario in order to earn the more money with the amount of fuel of his kart.

From a more general point of view, the problem is to find a path in a graph:
 - Path endpoints are given (from Mario's to Luigi's)
 - The sum of weights associated to arcs in the path is restricted (fuel consumption)
 - The sum of weights associated to nodes in the path has to be maximized (gold coins)

This problem was proposed by maury Ollagnier and Jean-Guillaume Fages.

## Data Example
  easy-2.json

## Model
  constraints: Circuit, Element, Sum, Table

## Execution
  python Mario.py -data=<datafile.json>
  python Mario.py -data=<datafile.json> -variant=table
  python Mario.py -data=<datafile.json> -variant=aux
  python Mario.py -data=<datafile.dzn> -parser=Mario_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  recreational, notebook
"""

from pycsp3 import *
from pycsp3.tools.curser import convert_to_namedtuples







def ref_model(param_dict):
    marioHouse = param_dict['marioHouse']
    luigiHouse = param_dict['luigiHouse']
    fuelLimit = param_dict['fuelLimit']
    nHouses = param_dict['nHouses']
    fuels = convert_to_namedtuples({"f":param_dict['fuels']}).f
    golds = param_dict['golds']
    #

    # marioHouse, luigiHouse, fuelLimit, houses = data
    # fuels, golds = zip(*houses)  # using cp_array is not necessary since intern arrays have the right type (for the constraint Element)
    # fuels = convert_to_namedtuples({"f":fuels}).f
    # nHouses = len(golds)

    # s[i] is the house succeeding to the ith house (itself if not part of the route)
    s = VarArray(size=nHouses, dom=range(nHouses))


    satisfy(
        # we cannot consume more than the available fuel
        Sum(fuels[i][s[i]] for i in range(nHouses)) <= fuelLimit,

        # Mario must make a tour (not necessarily complete)
        Circuit(s),

        # Mario's house succeeds to Luigi's house
        s[luigiHouse] == marioHouse
    )

    ## @variants removed


    maximize(
        # maximizing collected gold
        Sum((s[i] != i) * golds[i] for i in range(nHouses) if golds[i] != 0)
    )
    #
    return s, nHouses, golds

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
    s, nHouses, golds = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            s == dvar_dict["s"],
            Sum((s[i] != i) * golds[i] for i in range(nHouses) if golds[i] != 0) == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Sum((s[i] != i) * golds[i] for i in range(nHouses) if golds[i] != 0) > dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{sum((values(s)[i] != i) * golds[i] for i in range(nHouses) if golds[i] != 0)} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")





""" Comments
1) Note that the code below, when building the table is more compact than:
 [(s[i], f[i]) in [(j, houses[i].fuelConsumption[j]) for j in range(len(houses[i].fuelConsumption))] for i in range(nHouses)],
 or [(s[i], f[i]) in [(j, fuel) for j, fuel in enumerate(houses[i].fuelConsumption)] for i in range(nHouses)],

2) Note that introducing auxiliary variables for handling gold earned at each house could be as follows:
 # g[i] is the gold earned at house i
 g = VarArray(size=nHouses, dom=lambda i: {0, houses[i].gold})
 
  in that case, We need to introduce additional constraints, while the objective becomes:
 maximize(
   # maximizing collected gold
   Sum(g)
 )
"""

"""
/mario_medium_3.dzn = 1618 at the minizinc challenge 2017
but not the same bound with this Pycsp3 model

t = [5, 15]

cnt = 0
for row in fuels:
    m = min(v for v in row if v != 0)
    print("i ", m)
    cnt += m
print(cnt)
print(golds)
print(sum(golds), " ", sum(golds[i] for i in range(nHouses) if i not in t))

satisfy(
    [s[i] == i for i in t],
    [s[i] != i for i in range(nHouses) if i not in t]
)
"""