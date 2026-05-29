"""
The rectangle (square) packing problem consists of squares (bowes)
to be put in an enclosing rectangle (container) without overlapping of the squares.


## Data Example
  perfect-001.json

## Model
  constraints: NoOverlap

## Execution
  python RectPacking.py -data=<datafile.json>

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-85958-1_4

## Tags
  realistic
"""

from pycsp3 import *



def ref_model(param_dict):
  width, height = param_dict['container']
  box_widths = param_dict['widths']
  box_heights = param_dict['heights']
  #
  boxes = list(zip(box_widths, box_heights))
  nBoxes = len(boxes)
  #
  # x[i] is the x-coordinate where is put the ith rectangle
  x = VarArray(size=nBoxes, dom=range(width))

  # y[i] is the y-coordinate where is put the ith rectangle
  y = VarArray(size=nBoxes, dom=range(height))

  satisfy(
      # unary constraints on x
      [x[i] + box_widths[i] <= width for i in range(nBoxes)],

      # unary constraints on y
      [y[i] + box_heights[i] <= height for i in range(nBoxes)],

      # no overlap on boxes
      NoOverlap(
          origins=[(x[i], y[i]) for i in range(nBoxes)],
          lengths=boxes
      ),

      ## @symmetry-breaking removed
      # # tag(symmetry-breaking)
      # [
      #     x[-1] <= (width - box_widths[-1]) // 2,
      #     y[-1] <= x[-1]
      # ] if width == height else None
  )
  return x,y

""" Comments
1) Even if elements of boxes are named tuples, one can write length=boxes instead of lengths=[(w, h) for (w, h) in boxes]
2) See also CP papers on short supports
"""




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
    x, y = ref_model(param_dict)
    # verify satisfiability of the solution
    if args.check == 'sat':
        satisfy(
            x == dvar_dict["x"],
            y == dvar_dict["y"],
        )
        # display the result
        if solve() in [SAT, OPTIMUM]:
            print("sat@SAT")
        else:
            print("sat@UNSAT")