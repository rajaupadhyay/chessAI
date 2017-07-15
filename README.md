# chessAI
***
<p align="justify">
Built a chess AI that uses various heuristics to play decent chess.
The AI evaluates boards and positions using material score and piece square tables. It makes use of the mini-max algorithm with ALpha-Beta Pruning
to eliminate "bad moves". To avoid the Horizon problem i have made use of quiescence search with a minor tweaking of Delta pruning to ensure
the tree only expands up to a certain depth. Tested the engine against Stockfish - Can comfortably play and defeat the stockfish engine up to level 4 (out of 8 possible levels) with 
a win/loss ratio of 60/40. The engine easily loses in levels beyond 4 where the W/L ratio drops to around 35/65.
The engine was tested in 100 games at varying depths of minimax. 

The following are the future improvements i would like to work on:
1) Implement Razoring: Instead of skipping an entire subtree (what alpha beta does) i would like to search the subtree to a reduce depth: Ideally DEPTH-1.
This will help in redcuing the overall risk.
2) Transposition tables (dictionary/database that can store results of searches performed before to help save time by reducing the search space.
3) Improve the basic search function to allow larger depth searches.
4) Try implement the engine using Neural Networks when i actually understand how the work.
</p>
