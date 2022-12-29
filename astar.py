import argparse
import copy
import json
import time

def isValidGrid(grid):
    numTubes = len(grid)
    tubeHeight = max(len(t) for t in grid)
    numBalls = sum(len(t) for t in grid)
    numBallsRequired = (numTubes-2)*tubeHeight
    if (numBalls != numBallsRequired):
        print("Grid has incorrect number of balls")
        return False
    freqs = dict()
    for tube in grid:
        for ball in tube:
            if ball not in freqs:
                freqs[ball] = 1
            else:
                freqs[ball] += 1
    for colour,count in freqs.items():
        if count != tubeHeight:
            print("Expected "+str(tubeHeight)+" "+colour+" balls, found "+str(count))
            return False
    return True

def isSolved(grid, tubeHeight=None):
    if tubeHeight is None:
        tubeHeight = max(len(t) for t in grid)
    for tube in grid:
        if(len(tube) == 0):
            continue
        elif(len(tube) < tubeHeight):
            return False
        elif(tube.count(tube[0]) != tubeHeight): # elements in tube don't all match first elem
            return False
    return True

def loadGrid(filename):
    with open(filename) as json_file:
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


