import argparse
import copy
import time
import someConditions


def solvePuzzle(puzzle, bottleHeight=None, visitedPositions=set(), answer=[]):
    if bottleHeight is None: 
        bottleHeight = max(len(t) for t in puzzle)
    # If no bottleHeight is given, it sets the bottleHeight to the maximum length of the puzzle.
    visitedPositions.add(someConditions.puzzleToCanonicalString(puzzle))
    # This adds the puzzle to the set of visited positions, in canonical string form.
    queue = []
    # This creates an empty queue, which will be used to store puzzles that need to be evaluated.
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
                    queue.append(bottle2)
                    visitedPositions.add(someConditions.puzzleToCanonicalString(bottle2))
    # This loop iterates through the puzzle and checks if any moves are valid. 
    # If a move is valid, it will make the move and check if the puzzle is solved. 
    # If the puzzle is solved, it will add the solution to the answer and return True. 
    # If the puzzle is not solved, it will add the puzzle to the queue if it has not already been visited.
    while queue:
        currentPuzzle = queue.pop(0)
        solved = solvePuzzle(currentPuzzle, bottleHeight, visitedPositions, answer)
        if solved:
            answer.append(someConditions.printPuzzleToString(currentPuzzle))
            return True
    # This loop pops the first puzzle from the queue and attempts to solve it. 
    # If the puzzle is solved, it will add the solution to the answer and return True. 
    # If the puzzle is not solved, it will call the solvePuzzle function again with the current puzzle.
    return False
    # This returns False if the puzzle is not solved after all moves have been evaluated.



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
                
        
                
    