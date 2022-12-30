import argparse
import copy
import json
import time
import puzzles

def isValidPuzzle(puzzle): #to check if the puzzle is valid
    numBottles = len(puzzle)
    bottleHeight = max(len(t) for t in puzzle)
    numWaters = sum(len(t) for t in puzzle)
    numWatersRequired = (numBottles-2)*bottleHeight
    if (numWaters != numWatersRequired):
        print("Puzzle has incorrect number of waters")
        return False
    freq = dict()
    for bottle in puzzle:
        for water in bottle:
            if water not in freq:
                freq[water] = 1
            else:
                freq[water] += 1
    for color,count in freq.items():
        if count != bottleHeight:
            print("Expected "+str(bottleHeight)+" "+color+" waters, found "+str(count))
            return False
    return True

def isSolved(puzzle, bottleHeight=None):
    if bottleHeight is None:
        bottleHeight = max(len(t) for t in puzzle)
    for tube in puzzle:
        if(len(tube) == 0): 
            # there are 2 bottles must be empty when puzzle is solved
            continue
        elif(len(tube) < bottleHeight):
            # if there is a bottle is not full then the puzzle is not solved
            return False
        elif(tube.count(tube[0]) != bottleHeight): 
            # if the number of the same color is not equal to bottle's height then the puzzle is not solved
            return False
    return True

def loadPuzzle(filename):
    with open('puzzles/' + filename) as json_file:
        data = json.load(json_file)
        puzzle = data['bottles']
        return puzzle

def printPuzzleToString(puzzle): #to print bottles
    lines = []
    for bottle in puzzle:
        lines.append(''.join(bottle))
    return("\n".join(lines))

def isMoveValid(bottleHeight, fromBottle, candidateBottle):
    # move is valid if the source bottle isn't empty, the destination isn't full, 
    # and the water at the end of the source bottle is the same as the water at the end of the destination.
    if len(fromBottle) == 0 or len(candidateBottle) == bottleHeight:
        return False
    numFirstColor = fromBottle.count(fromBottle[0])
    if numFirstColor == bottleHeight: # bottle is full of same color, don't touch it
        return False
    if len(candidateBottle) == 0:
        if numFirstColor == len(fromBottle): # source bottle has all waters with the same color, so pointless moving to empty bottle
            return False
        return True
    return fromBottle[-1] == candidateBottle[-1]

def gridToCanonicalString(grid):
    tubeStrings = []
    for tube in grid:
        tubeStrings.append(','.join(tube))
    sortedTubeStrings = sorted(tubeStrings)
    return ';'.join(sortedTubeStrings)


def solvePuzzle(puzzle, bottleHeight=None, visitedPositions=set(), answer=[]):
    if bottleHeight is None:
        bottleHeight = max(len(t) for t in puzzle)
    # visitedPositions keeps track of all the states of the grid we have considered
    # to make sure we don't go round in circles
    # canonical (ordered) string representation of the grid means
    # that two grids that differ only by the order of the tubes are
    # considered as the same position
    visitedPositions.add(gridToCanonicalString(puzzle))
    for i in range(len(puzzle)):
        bottle = puzzle[i]
        for j in range(len(puzzle)):
            if i == j:
                continue
            candidateBottle = puzzle[j]
            if isMoveValid(bottleHeight, bottle, candidateBottle):
                grid2 = copy.deepcopy(puzzle)
                grid2[j].append(grid2[i].pop())
                if(isSolved(grid2, bottleHeight)):
                    answer.append(printPuzzleToString(grid2))
                    return True
                if(gridToCanonicalString(grid2) not in visitedPositions):
                    solved = solvePuzzle(grid2, bottleHeight, visitedPositions, answer)
                    if solved:
                        answer.append(printPuzzleToString(grid2))
                        return True
    return False



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="(Attempt to) solve a water sort puzzle")
    parser.add_argument("json",help="filename of input file (in JSON format)")
    parser.add_argument("--show-working", dest="working", help="Print out the steps to the solution", action='store_true')
    args = parser.parse_args()
    puzzle = loadPuzzle(args.json)
    start = time.time()
    if not isValidPuzzle(puzzle):
        exit("Invalid puzzle")
    if isSolved(puzzle):
        print("Puzzle is already solved")
        exit()
    print(printPuzzleToString(puzzle))
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



