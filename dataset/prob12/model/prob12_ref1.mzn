% source: water_buckets_regular.mzn
% MiniZinc model for the water buckets problem
%
% Model created by Hakan Kjellerstrand, hakank@gmail.com
% See also my MiniZinc page: http://www.hakank.org/minizinc

%
% Solution should be
%   x: [1, 9, 10, 11, 12, 13, 14, 15]
%   8,0,0 -> 3,5,0
%   3,5,0 -> 3,2,3
%   3,2,3 -> 6,2,0
%   6,2,0 -> 6,0,2
%   6,0,2 -> 1,5,2
%   1,5,2 -> 1,4,3
%   1,4,3 -> 4,4,0
% 
include "globals.mzn";

int: n_states ;
int: input_max ;
int: initial_state ;
set of int: accepting_states;


% distance
array[1..n_states, 1..n_states] of 0..input_max: transition_fn;


array[1..n_states] of string:  nodes;


array[1..input_max] of var 0..input_max: x;
var 0..input_max: cost;

% solve satisfy;
solve minimize cost;

constraint
regular(x, n_states, input_max, transition_fn,
        initial_state, accepting_states)
;

constraint
   cost = 2+sum([bool2int(x[i-1] != x[i] ) | i in 2..input_max])
;

output 
["cost: " ++ show(cost) ++ "\n"] ++
[show(initial_state) ++ " "] ++
[
  if fix(x[i]) < input_max then show(x[i]) ++ " " else " " endif
  | i in 1..input_max where fix(x[i]) < input_max
] ++ 
[show(input_max) ++ "\n"] ++ 
["\n\n"] ++

[show(nodes[initial_state]) ++ "\n"] ++
[
  if fix(x[i]) < input_max then show(nodes[fix(x[i])]) ++ "\n" else " " endif
  | i in 1..input_max where fix(x[i]) < input_max
] ++ 
[show(nodes[input_max]) ++ "\n"] ++ 
["\n"];

