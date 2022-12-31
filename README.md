# Water Sort Puzzle Solver
In this project, some basic AI knowledge are used to solve "Water Sort Puzzle".

This project is written in Python 3.10.
### Requirements
Firstly, you have to install Python: https://www.python.org/downloads/

In this project, we use argparse module to run in CLI.

If your PC/Mac don't have argparse module, you can install it via command:

``` 
pip install argparse 
```
### Introduction to important files and directories in the project
``` generator.py     ``` : The puzzle generator.

``` astar.py         ``` : The implementation of A* search.

``` bfs.py           ``` : The implementation of Breadth-first search.

``` dfs.py           ``` : The implementation of Depth-first search.

``` \puzzles         ``` : The folder contains all the generated puzzles.

``` \solutions\astar ``` : The folder contains solutions of  A* method. 

``` \solutions\bfs   ``` : The folder contains solutions of BFS method.

``` \solutions\dfs   ``` : The folder contains solutions of DFS method.


### Guide

#### The puzzle generator
You can generate a new puzzle via command in this project directory by using:

``` 
python generator.py xxx xxxx xxxxx.json 
```
    
- xxx is the number of bottles.
    
- xxxx is the number of waters in one bottle.
    
- xxxxx is the name of json file in which we save the puzzle.

After generated, the puzzle is saved in the folder 'puzzles'.

#### The puzzle solver
You can solve a puzzle in 'puzzles' folder via command in this project directory by using:

``` 
python xxx.py xxxx.json 
```

- xxx is the name of method you want to use to solve the puzzle. Here we have:
    - astar
    - bfs
    - dfs

- xxxx is the json file name of the puzzle you want to solve.

If you want to show the working process, use:

``` 
python xxx.py xxxx.json --show-working 
```

### Example
#### Puzzle 

This puzzle has 4 bottles that can contain 3 blocks of water, 2 bottles are full and 2 bottles are empty.

The same letters represent the same color.

Bottle here is similar to stack, the last element is the water on the top of the bottle.

```
{
   "bottles": [
      ["a", "b", "b"],
      ["b", "a", "a"],
      [],
      []
   ]
}
```

#### Solution

Solution of the above puzzle solved by A* algorithm.

Each line represents a bottle, empty lines represent empty bottles.

Each element of the bottle from bottom to top is represented in a line from left to right.

```
abb
baa


--
Visited 10 positions in 0.001 seconds
Solved in 6 moves
ab
baa
b

--
a
baa
b
b
--
aa
ba
b
b
--
aaa
b
b
b
--
aaa

bb
b
--
aaa

bbb

--
```

---
### Reference List

```
https://github.com/tjwood100/ball-sort-puzzle-solver

```
















