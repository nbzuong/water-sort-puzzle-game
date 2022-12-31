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
    for i in range(len(puzzle)):
        bottle = puzzle[i]
        for j in range(len(puzzle)):
            if i == j:
                continue
            candidateBottle = puzzle[j]
            if someConditions.isMoveValid(bottleHeight, bottle, candidateBottle):
                puzzle2 = copy.deepcopy(puzzle)
                puzzle2[j].append(puzzle2[i].pop())
                if(someConditions.isSolved(puzzle2, bottleHeight)):
                    answer.append(someConditions.printPuzzleToString(puzzle2))
                    return True
                if(someConditions.puzzleToCanonicalString(puzzle2) not in visitedPositions):
                    solved = solvePuzzle(puzzle2, bottleHeight, visitedPositions, answer)
                    if solved:
                        answer.append(someConditions.printPuzzleToString(puzzle2))
                        return True
    # Two for loops loop through the puzzle and 
    # set bottle and candidateBottle variables to the current bottle and the bottle to be compared.
    # Then check if the move is valid using the isMoveValid function from someConditions.
    # If isMoveValid is true, create a deep copy of the puzzle, and remove the last element from the current bottle and adds it to the candidateBottle.
    # After that move, check if the puzzle is solved using the isSolved function from someConditions.
    # Then check if the puzzle is in the set of visited positions, in canonical string form.
    # Call the solvePuzzle recursively with the updated puzzle, bottleHeight, visitedPositions, and answer.
    # Append the puzzle to the answer list, then return True if the puzzle is solved.
    return False
    # Else return False if the puzzle is not solved.



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



