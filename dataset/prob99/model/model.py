"""
PyCSP3 Model (see pycsp.org)

Examples:
  python SportsScheduling.py
  python SportsScheduling.py -data=10
  python SportsScheduling.py -data=10 -variant=dummy
"""

from pycsp3 import *

def ref_model(param_dict=None):
    nTeams = param_dict['n']
    nWeeks, nPeriods, nMatches = nTeams - 1, nTeams // 2, (nTeams - 1) * nTeams // 2
    # @@ modified to be consistent with output home/away instead of normalized smaller/larger team indexes
    # def match_number(t1, t2):
    #     return nMatches - ((nTeams - t1) * (nTeams - t1 - 1)) // 2 + (t2 - t1 - 1)


    # table = {(t1, t2, match_number(t1, t2)) for t1, t2 in combinations(range(nTeams), 2)}
    def match_number(t1, t2):
        return nMatches - ((nTeams - t1) * (nTeams - t1 - 1)) // 2 + (t2 - t1 - 1)

    def unordered_match_number(a, b):
        t1, t2 = min(a, b), max(a, b)
        return match_number(t1, t2)

    table = {
        (home, away, unordered_match_number(home, away))
        for home in range(nTeams)
        for away in range(nTeams)
        if home != away
    }

    # m[w][p] is the number of the match at week w and period p
    m = VarArray(size=[nWeeks, nPeriods], dom=range(nMatches))

    # x[w][p] is the first team for the match at week w and period p
    x = VarArray(size=[nWeeks, nPeriods], dom=range(nTeams))

    # y[w][p] is the second team for the match at week w and period p
    y = VarArray(size=[nWeeks, nPeriods], dom=range(nTeams))

    satisfy(
        # all matches are different (no team can play twice against another team)
        AllDifferent(m),

        # linking variables through ternary table constraints
        [(x[w][p], y[w][p], m[w][p]) in table for w in range(nWeeks) for p in range(nPeriods)],

        # each week, all teams are different (each team plays each week)
        [AllDifferent(x[w] + y[w]) for w in range(nWeeks)],

        # each team plays at most two times in each period
        [Cardinality(x[:, p] + y[:, p], occurrences={t: range(1, 3) for t in range(nTeams)}) for p in range(nPeriods)],

        ## @symmetry-breaking removed
        # # tag(symmetry-breaking)
        # [
        #     # the match '0 versus t' (with t strictly greater than 0) appears at week t-1
        #     [Count(m[w], value=match_number(0, w + 1)) == 1 for w in range(nWeeks)],

        #     # the first week is set : 0 vs 1, 2 vs 3, 4 vs 5, etc.
        #     [m[0][p] == match_number(2 * p, 2 * p + 1) for p in range(nPeriods)]
        # ]
    )
    #
    return m,x,y

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
    m,x,y = ref_model(param_dict)
    import numpy as np
    # m = (np.array(m)-1).tolist()
    # x_ = (np.array(dvar_dict["x"])-1).tolist()
    # y_ = (np.array(dvar_dict["y"])-1).tolist()
    # print(x_)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            m == dvar_dict["m"],
            x == dvar_dict["x"],
            y == dvar_dict["y"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")


# invalid solution due to order
# {'m': [[26, 13, 11, 3],
#   [23, 15, 6, 8],
#   [25, 12, 14, 2],
#   [18, 5, 17, 10],
#   [0, 21, 22, 16],
#   [1, 9, 19, 27],
#   [7, 4, 20, 24]],
#  'x': [[7, 2, 1, 0],
#   [4, 2, 0, 1],
#   [5, 1, 2, 0],
#   [3, 0, 2, 1],
#   [0, 3, 4, 2],
#   [0, 1, 3, 6],
#   [1, 0, 3, 4]],
#  'y': [[5, 3, 6, 4],
#   [6, 5, 7, 3],
#   [6, 7, 4, 3],
#   [4, 6, 7, 5],
#   [1, 7, 5, 6],
#   [2, 4, 5, 7],
#   [2, 5, 6, 7]]}