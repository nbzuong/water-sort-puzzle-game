# Water Sort Puzzle Solver
This project is using some basic AI knowledge to solve "Water Sort Puzzle".

Here we use Python 3.10 to write this project.
### Requirements
Firstly, you have to install Python: https://www.python.org/downloads/

In this project, we use argparse module to run in CLI.

If your PC/Mac don't have argparse module, you can install it via command:

``` 
pip install argparse 
```
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

#### The solver
You can solve a puzzle in 'puzzles' folder via command in this project directory by using:

``` 
python xxx.py xxxx.json 
```

- xxx is the name of method you want to use to solve the puzzle. Here we have:
    - astar.py is using A* search algorithm.
    - bfs.py is using Breadth-first search algorithm.
    - dfs.py is using Depth-first search algorithm.

- xxxx is the json file name of the puzzle you want to solve.

If you want to show the working process, use:

``` 
python xxx.py xxxx.json --show-working 
```















