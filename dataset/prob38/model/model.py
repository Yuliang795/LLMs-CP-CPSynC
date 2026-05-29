"""
Verbal arithmetic, also known as alphametics, cryptarithmetic, cryptarithm or word addition, is a type of mathematical game
consisting of a mathematical equation among unknown numbers, whose digits are represented by letters of the alphabet.

### Example
  For the Puzzle:
  ```
       S E N D
   +   M O R E
   = M O N E Y
  ```
  a possible solution is:
  ```
       9 5 6 7
   +   1 0 8 5
   = 1 0 6 5 2
  ```

## Data
  Three strings/words (as for example [send,more,money])

## Model
  There are a main variant and a variant involving carry variables.
  You can also find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/CryptoPuzzle/).

  constraints: AllDifferent, Sum

## Execution
  python CryptoPuzzle.py -data=[string,string,string]
  python CryptoPuzzle.py -data=[string,string,string] -variant=carry

## Links
  - https://en.wikipedia.org/wiki/Verbal_arithmetic

## Tags
  academic, notebook
"""

from pycsp3 import *

def ref_model(param_dict):
    word1, word2, word3 = words = [w.lower() for w in param_dict.values()] if param_dict else ("no", "no", "yes")
    n = len(word1)
    assert len(word2) == n and len(word3) in {n, n + 1}

    # x[i] is the value assigned to the ith letter (if present) of the alphabet
    ## asign a number [0-9] to used letters only 
    x = VarArray(size=26, dom=lambda i: range(10) if i in alphabet_positions(words) else None)

    # auxiliary lists of variables associated with the three words
    x1, x2, x3 = [x[reversed(alphabet_positions(word))] for word in words]

    satisfy(
        # all letters must be assigned different values
        AllDifferent(x),

        # the most significant letter of each word cannot be equal to 0
        [
            x1[-1] != 0,
            x2[-1] != 0,
            x3[-1] != 0
        ]
    )

    satisfy(
        # ensuring the crypto-arithmetic sum
        Sum((x1[i] + x2[i]) * 10 ** i for i in range(n))
        ==
        Sum(x3[i] * 10 ** i for i in range(len(x3)))
    )
    #
    return x,x1,x2,x3

## @variant removed
# elif variant("carry"):
#     # c[i] is the ith carry
#     c = VarArray(size=n + 1, dom={0, 1})

#     satisfy(
#         # managing the least significant carry
#         c[0] == 0,

#         # managing the most significant carry
#         c[n] == (0 if len(x3) == n else x3[n]),  # NB: the parentheses are required

#         # managing remainders
#         [(c[i] + x1[i] + x2[i]) % 10 == x3[i] for i in range(n)],

#         # managing quotients
#         [(c[i] + x1[i] + x2[i]) // 10 == c[i + 1] for i in range(n)]
#     )



"""
1) Example of data: (no,no,yes) (two,two,four) (send,more,money) (cross,road,danger) (donald,gerald,robert)
2) Note that:
 x[reversed(alphabet_positions(word))]
   is equivalent to: 
 [x[i] for i in reversed(alphabet_positions(word))]
"""
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
    # prepare decision variables
    x,x1,x2,x3 = ref_model(param_dict)
    x_sol = dvar_dict["x"]
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            [x[i] == x_sol[i] for i in range(26) if x_sol[i] is not None],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")

    # verify optimality of the solution
    elif args.check == 'opt':
        pass