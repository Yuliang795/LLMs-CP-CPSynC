% source: K4xP2Graceful.mzn
% K4P2 Graceful Graph in MiniZinc.
% 
% Problem from Minion summer_school/examples/K4P2GracefulGraph.eprime
% 
% This is a more general model than K4P2GracefulGraph.mzn
% 
% Model created by Hakan Kjellerstrand, hakank@bonetmail.com
% See also my MiniZinc page: http://www.hakank.org/minizinc

include "globals.mzn"; 

int: m;
int: n;
array[1..n] of var 0..m: nodes;
array[1..m] of var 1..m: edges;
array[1..m, 1..2] of var 1..n: graph;




solve :: int_search(nodes, first_fail, indomain_min, complete) satisfy;

constraint
  forall(i in 1..m) (
    abs(nodes[graph[i,1]] - nodes[graph[i,2]]) = edges[i]  
  )
  /\
  all_different(edges) 
  /\ 
  all_different(nodes)
;


% output
% [
%   "nodes: " ++ show(nodes) ++ "\n" ++
%   "edges: " ++ show(edges) ++ "\n"
% ];