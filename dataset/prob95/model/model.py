"""
One morning, in 1880, four families (the Boyds, Garveys, Logans and Navarros) stopped by Purdey's general store.
Each family bought a different item: 50 pounds of flour, two gallons of kerosene, ten yards of muslin cloth, ten pounds of sugar.
One family paid cash, one took the item on credit and the other two traded other items for it (one a cured ham and the other a bushel of peas).
We know that:
 - the Boyds were new in town, and this was their first visit to the store
 - the family (which wasn't the Logans) that traded the bushel of peas didn't buy the kerosene
 - the Boyds and the Garveys bought the kerosene and the muslin in some order
 - one family traded a cured ham for a large sack of flour
 - Purdey only extended credit to regular customers, such as the family that bought the muslin on credit

## Data
  all integrated (single problem)

## Model
  constraints: AllDifferent

## Execution
  python Purdey.py

## Tags
  single
"""

from pycsp3 import *

def ref_model(param_dict=None):
  families = Boyds, Garveys, Logans, Navarros = "Boyds", "Garveys", "Logans", "Navarros"

  flour = Var(families)
  kerosene = Var(families)
  cloth = Var(families)
  sugar = Var(families)

  cash = Var(families)
  credit = Var(families)
  ham = Var(families)
  peas = Var(families)

  satisfy(
      AllDifferent(flour, kerosene, cloth, sugar),
      AllDifferent(cash, credit, ham, peas),
      peas != Logans,
      peas != kerosene,
      either(kerosene == Boyds, cloth == Boyds),
      either(kerosene == Garveys, cloth == Garveys),
      ham == flour,
      credit == cloth,
      credit != Boyds
  )
  #
  return [flour, kerosene, cloth, sugar], [cash, credit, ham, peas] 


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
    item_buyer, payment_family = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            (item_buyer[i] == dvar_dict["item_buyer"][i] for i in range(4)),
            (payment_family[i] == dvar_dict["payment_family"][i] for i in range(4)),
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")