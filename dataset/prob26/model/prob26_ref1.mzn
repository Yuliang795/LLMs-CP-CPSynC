% source: queens3.mzn
% n queens problem in MiniZinc.
% 
% This MiniZinc model was created by Hakan Kjellerstrand, hakank@gmail.com
% See also my MiniZinc page: http://www.hakank.org/minizinc
%

% Licenced under CC-BY-4.0 : http://creativecommons.org/licenses/by/4.0/

% include needed libraries
include "globals.mzn";
% load parameters
int: n;
% instantiate decision variables, each queen is in a different row
array[1..n] of var 1..n: queens;

% no two queens in the same column
constraint all_different(queens);
% no two queens in the same column or diagonal
constraint
    forall(i, j in 1..n where i < j) (
         queens[i] != queens[j] /\
         queens[i] + i != queens[j] + j /\
         queens[i] - i != queens[j] - j
    ) 
 ;

solve satisfy;

% solve :: int_search(
%         queens, 
%         first_fail, 
%         indomain_min, 
%         complete) 
%     satisfy;


% data
% n = 4;





