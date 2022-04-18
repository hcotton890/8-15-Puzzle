# 8-Puzzle & 15-Puzzle Project 

Group Members: Hunter Cotton, Chris Kuramoto, Lee Xiong

State-based search algorithms:
- Breadth-First Search
- Depth-First Search
- Iterative-Deepening Depth-First Search
- A* w/ Out-of-Place, and Manhattan Distance Heuristics
- Iterative Deepening A* w/ Out-of-Place and Manhattan Distance Heuristics

Main.py is the file for 8-puzzle
Running code: python main.py {algorithm as string} {start_state as string}
algorithm = bfs, dfs, ids, a_star, or ida_star

example - python main.py bfs 123456870

Note: Goal state is already set to 123456780

search15.py is the file for 15-puzzle
Running code: python search15.py {algorithm as string} {start_state as string}
algorithm = bfs, dfs, ids, a_star, or ida_star

example - python search15.py bfs 1234568789ABCEDF0

applymoves.py is the file for applying movement manually
Running code: python applymoves.py {Current State of graph} {moves to apply}
moves possible = l r u d
example - applymoves.py 012345678 lrdlru

applymoves15.py is the file for applying movement manually
Running code: python applymoves.py {Current State of graph} {moves to apply}
moves possible = l r u d
example - applymoves.py 0123456789ABCDEF lrdlru
