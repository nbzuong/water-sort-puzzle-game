import argparse
import copy
import json
import time
import puzzles

def isValidPuzzle(puzzle):
    numBottles = len(puzzle)
    bottleHeight = max(len(t) for t in puzzle)
    numWaters = sum(len(t) for t in puzzle)
    numWatersRequired = (numBottles-2)*bottleHeight
    if (numWaters != numWatersRequired):
        print("Puzzle has incorrect number of waters")
        return False
    freqs = dict()
    for bottle in puzzle:
        for water in bottle:
            if water not in freqs:
                freqs[water] = 1
            else:
                freqs[water] += 1
    for color,count in freqs.items():
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
            # if there is a bottle is not filled then the puzzle is not solved
            return False
        elif(tube.count(tube[0]) != bottleHeight): 
            # if the number of the same color is not equal to bottle's height then the puzzle is not solved
            return False
    return True

def loadGrid(filename):
    with open('puzzles/' + filename) as json_file:
        data = json.load(json_file)
        grid = data['tubes']
        return grid

def printGridToString(grid):
    lines = []
    for tube in grid:
        #print(tube)
        lines.append(''.join(tube))
    return("\n".join(lines))

def isMoveValid(tubeHeight, fromTube, candidateTube):
    # move is valid if the source tube isn't empty,
    # the destination isn't full,
    # and the ball at the end of the source tube is the same as the
    # ball at the end of the destination.
    # But there are also some optimizations to avoid pointless moves.
    if len(fromTube) == 0 or len(candidateTube) == tubeHeight:
        return False
    numFirstColour = fromTube.count(fromTube[0])
    if numFirstColour == tubeHeight: # tube is full of same colour, don't touch it
        return False
    if len(candidateTube) == 0:
        if numFirstColour == len(fromTube): # source tube all the same colour, so pointless moving to empty tube
            return False
        return True
    return fromTube[-1] == candidateTube[-1]

def gridToCanonicalString(grid):
    tubeStrings = []
    for tube in grid:
        tubeStrings.append(','.join(tube))
    sortedTubeStrings = sorted(tubeStrings)
    return ';'.join(sortedTubeStrings)


def solveGrid(grid, tubeHeight=None, visitedPositions=set(), answer=[]):
    if tubeHeight is None:
        tubeHeight = max(len(t) for t in grid)
    # visitedPositions keeps track of all the states of the grid we have considered
    # to make sure we don't go round in circles
    # canonical (ordered) string representation of the grid means
    # that two grids that differ only by the order of the tubes are
    # considered as the same position
    visitedPositions.add(gridToCanonicalString(grid))
    for i in range(len(grid)):
        tube = grid[i]
        for j in range(len(grid)):
            if i == j:
                continue
            candidateTube = grid[j]
            if isMoveValid(tubeHeight, tube, candidateTube):
                grid2 = copy.deepcopy(grid)
                grid2[j].append(grid2[i].pop())
                if(isSolved(grid2, tubeHeight)):
                    answer.append(printGridToString(grid2))
                    return True
                if(gridToCanonicalString(grid2) not in visitedPositions):
                    solved = solveGrid(grid2, tubeHeight, visitedPositions, answer)
                    if solved:
                        answer.append(printGridToString(grid2))
                        return True
    return False



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="(Attempt to) solve a ball sort puzzle")
    parser.add_argument("json",help="filename of input file (in JSON format)")
    parser.add_argument("--show-working", dest="working", help="Print out the steps to the solution", action='store_true')
    args = parser.parse_args()
    grid = loadGrid(args.json)
    start = time.time()
    if not isValidGrid(grid):
        exit("Invalid grid")
    if isSolved(grid):
        print("Grid is already solved")
        exit()
    print(printGridToString(grid))
    print("--")
    answer = []
    visitedPositions = set()
    solved = solveGrid(grid, visitedPositions=visitedPositions, answer=answer)
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



