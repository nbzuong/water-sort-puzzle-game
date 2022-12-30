import argparse
import copy
import time
import someConditions
from queue import PriorityQueue


def solvePuzzle(puzzle, bottleHeight=None, visitedPositions=set(), answer=[]):
    if bottleHeight is None:
        bottleHeight = max(len(t) for t in puzzle)
    visitedPositions.add(someConditions.puzzleToCanonicalString(puzzle))
    priorityQueue = PriorityQueue()
    for i in range(len(puzzle)):
        bottle = puzzle[i]
        for j in range(len(puzzle)):
            if i == j:
                continue
            candidateBottle = puzzle[j]
            if someConditions.isMoveValid(bottleHeight, bottle, candidateBottle):
                bottle2 = copy.deepcopy(puzzle)
                bottle2[j].append(bottle2[i].pop())
                if(someConditions.isSolved(bottle2, bottleHeight)):
                    answer.append(someConditions.printPuzzleToString(bottle2))
                    return True
                if(someConditions.puzzleToCanonicalString(bottle2) not in visitedPositions):
                    priorityQueue.put((getHeuristic(bottle2, bottleHeight), bottle2))
                    visitedPositions.add(someConditions.puzzleToCanonicalString(bottle2))
    while not priorityQueue.empty():
        currentPuzzle = priorityQueue.get()[1]
        solved = solvePuzzle(currentPuzzle, bottleHeight, visitedPositions, answer)
        if solved:
            answer.append(someConditions.printPuzzleToString(currentPuzzle))
            return True
    return False

def getHeuristic(puzzle, bottleHeight):
    # heuristic is the number of balls that are not in the correct tube
    totalWaters = (bottleHeight * len(puzzle)) - (len(puzzle) - 2)
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