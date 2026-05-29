"""
Deriving the optimal wiring sequence for a given layout of a cable tree.
See paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  A031.json

## Model
  constraints: Maximum, Sum

## Execution
  python CableTreeWiring.py -data=<datafile.json>
  python CableTreeWiring.py -data=<datafile.dzn> -parser=CableTreeWiring_ParserZ.py

## Links
  - https://link.springer.com/article/10.1007/s10601-021-09321-w
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
"""

from pycsp3 import *






def ref_model(param_dict):
  k= param_dict['k']
  b= param_dict['b']
  atomic= param_dict['atomic']
  disjunctive= param_dict['disjunctive']
  soft= param_dict['soft']
  direct= param_dict['direct']
  #
  assert b > 0 and isinstance(direct, list), str(direct)

  # x[i] is the position of the ith cavity
  x = VarArray(size=k, dom=range(k))

  satisfy(
      AllDifferent(x),

      [x[i] < x[j] for i, j in atomic],

      [
          either(
              x[i] < x[j],
              x[k] < x[l]
          ) for i, j, k, l in disjunctive
      ],

      [
          If(
              x[j] < x[j + b],
              Then=x[j] + 1 == x[j + b]
          ) for j in direct if j < b
      ],

      [
          If(
              x[j] < x[j - b],
              Then=x[j] + 1 == x[j - b]
          ) for j in direct if j >= b
      ],

      [
          either(
              x[i] < x[j],
              x[i] < x[l]
          ) for i, j, k, l in disjunctive if i == k
      ]
  )

  tmp = [[both(x[j] < x[i], x[i] < x[j + g]) for j in range(2 * b) for g in [b if j < b else -b] if i not in {j, j + g}] for i in range(2 * b)]



  ## @auxiliary variables for evaluation
  Z = Var(dom=range(0, 999999))
  satisfy(
      Z == (
          Sum(abs(x[i] - x[i + b]) > 1 for i in range(b)) * k ** 3
          +
          Maximum(Sum(t) for t in tmp) * k ** 2
          +
          Maximum(abs(x[i] - x[i + b]) - 1 for i in range(b)) * k
          +
          Sum(x[i] > x[j] for i, j in soft)
      ),
  )
  minimize(Z)
  #
  return x,Z


"""
1) note that:
 either(x[i] < x[j], x[k] < x[l])
  is equivalent to:
   (x[i] < x[j]) | (x[k] < x[l])
2) note that:
  both(x[j] < x[i], x[i] < x[j + g])
   is equivalent to:
  (x[j] < x[i]) & (x[i] < x[j + g])
3) a useless array is present in the minizinc model.
 if variant("mz"):
     y = VarArray(size=k, dom=range(k))

     satisfy(
         AllDifferent(y)
     )
"""

# minimize(
#     Sum(
#         [k ** 3 * (abs(x[i] - x[i + b]) > 1) for i in range(b)],
#         Maximum((Sum(t) for t in tmp)) * k ** 2,
#         [Maximum(abs(x[i] - x[i + b]) - 1 for i in range(b)) * k],
#         [x[i] > x[j] for i, j in soft]
#     )
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
    print(dvar_dict)
    print(param_dict)
    #
    x,Z = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            [x[i] == dvar_dict["x"][i] for i in range(len(x))],
            Z == dvar_dict["z"]
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        satisfy(
            Z < dvar_dict["z"]
            )
        
        if solve() in [SAT, OPTIMUM]:
            print(f"opt@SUBOPT |  |ref:{value(Z)} - sol:{dvar_dict['z']}")
        else:
            print("opt@OPT")