% source: langford2.mzn
% Langford's number problem in MiniZinc.
%
% This model is based on the EssencePrime model in the Minion Translator examples:
%
% http://www.cs.st-andrews.ac.uk/~andrea/examples/langford/langford.eprime
% """
% Langford's number problem (CSP lib problem 24)
%
% Arrange 2 sets of positive integers 1..n to a sequence,
% such that, following the first occurence of an integer i, 
% each subsequent occurrence of i, appears i+1 indices later
% than the last. 
% For example, for n=4, a solution would be 41312432
% """
% 
% Also see: http://www.csplib.org/Problems/prob024/
%
% However, I added a better representation were we see the numbers in their
% proper positions: the solution array.
%  
% Model created by Hakan Kjellerstrand, hakank@gmail.com
% See also my MiniZinc page: http://www.hakank.org/minizinc
%

% Licenced under CC-BY-4.0 : http://creativecommons.org/licenses/by/4.0/

%
% Solution for n = 4:
% [4, 1, 3, 1, 2, 4, 3, 2]
%

include "globals.mzn";

int: k;
int: n;
set of int: positionDomain = 1..k*n;

array[positionDomain] of var positionDomain: position;
% better presentation:
array[positionDomain] of var 1..n: solution;

solve :: int_search(position, first_fail, indomain_min, complete) satisfy;

constraint
  forall(i in 1..n) (
     position[i+n] = position[i] + i+1 /\
     % hakank: added this
     solution[position[i]] = i /\ 
     solution[position[n+i]] = i
  )
  /\   
  all_different(position)
  %% @symmetry-breaking removed
  % /\ % symmetry breaking
  % solution[1] < solution[2*n]
;


output [
  show(solution), "\n"

];

%
% data
%
% n = 4;
% n = 7;
% n = 8;
% n = 10;
% n = 20;
