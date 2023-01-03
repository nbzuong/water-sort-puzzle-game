import argparse
import copy
import time
import someConditions
from queue import PriorityQueue

import sys
sys.setrecursionlimit(2500)
# The more difficult the puzzle is, the more recursive steps it takes.
# So we do this to make sure the recursion error will not appear when solve expert+ level puzzles.


def solvePuzzle(puzzle, bottleHeight=None, visitedPositions=set(), answer=[]):
    if bottleHeight is None: 
        bottleHeight = max(len(t) for t in puzzle)
    # If no bottleHeight is given, it sets the bottleHeight to the maximum length of the puzzle.
    visitedPositions.add(someConditions.puzzleToCanonicalString(puzzle))
    # This adds the puzzle to the set of visited positions, in canonical string form.
    priorityQueue = PriorityQueue()
    # This line creates a priority queue, which is used to store puzzle configurations.
    for i in range(len(puzzle)):
        bottle = puzzle[i]
        for j in range(len(puzzle)):
            if i == j:
                continue
            candidateBottle = puzzle[j]
            if someConditions.isMoveValid(bottleHeight, bottle, candidateBottle):
                bottle2 = copy.deepcopy(puzzle)
                bottle2[j].append(bottle2[i].pop())
                if(someConditions.isSolved(bottle2)):
                    answer.append(someConditions.printPuzzleToString(bottle2))
                    return True
                if(someConditions.puzzleToCanonicalString(bottle2) not in visitedPositions):
                    priorityQueue.put((getHeuristic(bottle2, bottleHeight), bottle2))
                    visitedPositions.add(someConditions.puzzleToCanonicalString(bottle2))
    # This code loops through each bottle in the puzzle and comparing it to every other bottle in the puzzle. 
    # If the move is valid, it creates a deep copy of the puzzle 
    # and appends the bottle it was comparing to the bottle it was looping through. 
    # It then checks if the puzzle is solved. 
    # If the puzzle is not solved, it adds it to a priority queue and adds it to the list of visited positions.
    while not priorityQueue.empty():
        currentPuzzle = priorityQueue.get()[1]
        solved = solvePuzzle(currentPuzzle, bottleHeight, visitedPositions, answer)
        if solved:
            answer.append(someConditions.printPuzzleToString(currentPuzzle))
            return True
    # The while loop checks if the priority queue is empty. 
    # If it is not empty, it gets the current puzzle from the priority queue and calls the solvePuzzle() function on it. 
    # If the puzzle is solved, it adds the puzzle to the answer list and returns true. 
    # If the puzzle is not solved, it continues the loop until the priority queue is empty.
    return False
    # This line returns False if the puzzle is not solved.

def getHeuristic(puzzle, bottleHeight):
    # heuristic is the number of waters that are not in the correct bottle
    totalWaters = bottleHeight*(len(puzzle) - 2)
    numCorrectWaters = 0
    for bottle in puzzle:
        if len(bottle) > 0:
            if bottle.count(bottle[0]) == len(bottle):
                numCorrectWaters += len(bottle)
    return totalWaters - numCorrectWaters
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="(Attempt to) solve a water sort puzzle")
    parser.add_argument("json",help="filename of input file (in JSON format)")
    parser.add_argument("--show-working", dest="working", help="Print out the steps to the solution", action='store_true')
    args = parser.parse_args()
    puzzle = someConditions.loadPuzzle(args.json)
    start = time.time()
    if not someConditions.isValidPuzzle(puzzle):
        exit("Invalid puzzle")
    if someConditions.isSolved(puzzle):
        print("Puzzle is already solved")
        exit()
    print(someConditions.printPuzzleToString(puzzle))
    print("--")
    answer = []
    visitedPositions = set()
    solved = solvePuzzle(puzzle, visitedPositions=visitedPositions, answer=answer)
    end = time.time()
    print("Visited "+str(len(visitedPositions))+" positions in "+str(round(end-start, 3))+" seconds")
    if not solved:
        print("No solution")
    else:
        print("Solved in "+str(len(answer))+" moves")
        if(args.working):
            answer.reverse()
            for step in answer:
                print(step)
                print('--')
