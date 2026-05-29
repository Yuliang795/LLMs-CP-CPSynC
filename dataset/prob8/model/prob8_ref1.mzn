% This model is modified based on the original Nonogram model proivded in CSPLib
% 

include "globals.mzn";

int: rows;
int: row_rule_len;
array[1..rows, 1..row_rule_len] of int: row_rules;

int: cols;
int: col_rule_len;
array[1..cols, 1..col_rule_len] of int: col_rules;

% 1 = white, 2 = black
array[1..rows, 1..cols] of var 1..2: x;

predicate line_matches(array[int] of var int: line, array[int] of int: clues) =
  let {
    int: m = length(line),
    int: n = length(clues),
    int: nb = sum(k in 1..n)(bool2int(clues[k] > 0))
  } in
  if nb = 0 then
    forall(p in 1..m)(line[p] = 1)
  else
    let {
      array[1..nb] of int: c = [clues[k] | k in 1..n where clues[k] > 0];
      array[1..nb] of var 1..m: s
    } in
      % each block must fit in the line
      forall(k in 1..nb)(
        s[k] + c[k] - 1 <= m
      )
      /\
      % blocks must appear in order with at least one white cell between them
      forall(k in 1..nb-1)(
        s[k] + c[k] <= s[k+1] - 1
      )
      /\
      % a cell is black iff it is covered by some block
      forall(p in 1..m)(
        (line[p] = 2) <->
        exists(k in 1..nb)(
          s[k] <= p /\ p < s[k] + c[k]
        )
      )
  endif;

constraint
  forall(i in 1..rows)(
    line_matches(
      [x[i, j] | j in 1..cols],
      [row_rules[i, k] | k in 1..row_rule_len]
    )
  )
  /\
  forall(j in 1..cols)(
    line_matches(
      [x[i, j] | i in 1..rows],
      [col_rules[j, k] | k in 1..col_rule_len]
    )
  );

solve :: int_search(
  [x[i, j] | i in 1..rows, j in 1..cols],
  first_fail,
  indomain_min,
  complete
) satisfy;