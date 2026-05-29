"""
A Bin Packing Problem.

The bin packing problem (BPP) can be informally defined in a very simple way.
We are given n items, each having an integer weight wj (j = 1, ..., n), and an unlimited number of identical bins of integer capacity c.
The objective is to pack all the items into the minimum number of bins so that the total weight packed in any bin does not exceed the capacity.

## Data Example
  n1c1w4a.json

## Model
  There are two variants:
   - one with extension constraints
   - one with sum and decreasing constraints.

  constraints: BinPacking, Cardinality, Lex, Sum, Table

## Execution
  python BinPacking.py -data=<datafile.json>
  python BinPacking.py -data=<datafile.json> -variant=table

## Links
  - https://site.unibo.it/operations-research/en/research/bpplib-a-bin-packing-problem-library
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  recreational, xcsp24
"""

from pycsp3 import *
from itertools import groupby
from math import ceil


def ref_model(param_dict):
    binCapacity = param_dict['binCapacity']
    itemWeights= param_dict['itemWeights']# convert_to_namedtuples({"iw":param_dict['itemWeights']}).iw

    capacity, weights = binCapacity, itemWeights  # bin capacity and item weights
    weights.sort()  # in case weights are not sorted
    nItems = len(weights)


    # def n_bins():
    #     cnt = 0
    #     curr_load = 0
    #     for i, weight in enumerate(weights):
    #         curr_load += weight
    #         if curr_load > capacity:
    #             cnt += 1
    #             curr_load = weight
    #     return cnt
    #
    # updated to take the last bin into account
    def n_bins():
        cnt = 0
        curr_load = 0

        for weight in weights:
            if curr_load + weight > capacity:
                cnt += 1
                curr_load = weight
            else:
                curr_load += weight

        if curr_load > 0:
            cnt += 1

        return cnt


    def max_items_per_bin():
        curr = 0
        for i, weight in enumerate(weights):
            curr += weight
            if curr > capacity:
                return i
        return -1


    def w(a, b, *, bar=False):
        if bar:
            return [i for i, weight in enumerate(weights) if a <= weight <= b]
        return [i for i, weight in enumerate(weights) if a < weight <= b]


    def lb2(v=None):
        half = len(w(capacity // 2, capacity))
        if v is None:
            return max(lb2(vv) for vv in range(capacity // 2 + 1))
        return half + max(0, ceil(sum(weights[i] for i in w(v, capacity - v, bar=True)) / capacity - len(w(capacity // 2, capacity - v))))


    nBins, maxPerBin = n_bins(), max_items_per_bin()

    # x[i][j] is the weight of the jth object put in the ith bin. It is 0 if less than j objects are present in the bin.
    x = VarArray(size=[nBins, maxPerBin], dom={0, *weights})

    # z is the number of used bins
    z = Var(range(lb2(), nBins + 1))

    if not variant():
        satisfy(
            # not exceeding the capacity of each bin
            [Sum(x[i]) <= capacity for i in range(nBins)],

            # items are stored decreasingly in each bin according to their weights
            [Decreasing(x[i]) for i in range(nBins)]
        )



    satisfy(
        # computing the number of used bins
        z == Sum(x[i][0] != 0 for i in range(nBins)),

        # ensuring that each item is stored in a bin
        Cardinality(
            within=x,
            occurrences={0: nBins * maxPerBin - nItems} | {wgt: len(list(t)) for wgt, t in groupby(weights)}
        ),

        ## @symmetry-breaking removed
        # # tag(symmetry-breaking)
        # LexDecreasing(x)
    )

    minimize(
        # minimizing the number of used bins
        z  # Sum(x[i][0] != 0 for i in range(nBins))
    )

    # maximize(
    #     Sum(x[i][0] == 0 for i in range(nBins))
    # )
    #
    return x,z,nBins,maxPerBin,capacity,weights


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
    print(dvar_dict)
    #
    x,z,nBins,maxPerBin,capacity,weights = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
            z == dvar_dict["z"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            z < dvar_dict["z"],
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{value(z)} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")

