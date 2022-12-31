import argparse
import random
import json
import string
import puzzles

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a random permutation of waters in bottles")
    parser.add_argument("colors", help="number of colors", type=int)
    parser.add_argument("height", help="height of bottles", type=int)
    parser.add_argument("json", help="output filename (will be written in JSON format)")
    args = parser.parse_args()
    if(args.colors < 2 or args.colors > 52):
        exit("Colors must be between 2-52")
    if(args.height < 2):
        exit("Height must be 2 or more")

    l = []
    for i in range(args.colors):
        color = string.ascii_letters[i]
        cs = [color]*args.height
        l += cs
    random.shuffle(l)

    puzzle = []
    pos = 0
    for i in range(args.colors):
        puzzle.append(l[pos:pos+args.height])
        pos += args.height
    puzzle.append([])
    puzzle.append([])

    obj = dict()
    obj["bottles"] = puzzle

    with open(f'puzzles/' +args.json, 'w') as json_file:
        json.dump(obj, json_file, indent=3)