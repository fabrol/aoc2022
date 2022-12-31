from collections import defaultdict
from typing import Counter, Dict, List, Tuple
import logging
import sys
import itertools
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        return lines

'''
Store a map from pos of T,H (2-d delta of T from H), final relative pos of H or moves taken; to T at the end.
Build this up for basic movements, or let it get built up over time.
Then look up current position and highest possible moves match and simulate the rest
'''

DIR_MAP = {
    'U': (0,+1),
    'D': (0,-1),
    'R': (+1,0),
    'L': (-1,0),
}
def run_part_a(filename):
    movements = read_input(filename)
    # Init grid and cache
    PositionType = Tuple[Tuple[int, int], Tuple[int, int]]
    cache: Dict[Tuple[PositionType, Tuple[str, int]], PositionType] = {}
    pos: PositionType = ((0,0), (0,0)) # (H, T)

    for m in movements:
        dir, amt = m.split()
        dir_delta = DIR_MAP[dir]
        new_pos = pos

        for step in range(1, int(amt)+1):
            temp_pos = new_pos
            temp_pos[0] += 
            

            pass



def run_part_b(filename):
    fp = open(filename, 'r')
    pass


def test_part_a():
    expected = 5353
    actual = run_part_a('test9.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


def test_part_b():
    expected = 5353
    actual = run_part_b('test9.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


test_part_a()
print(f"Part A: {run_part_a('day9.in')}")

test_part_b()
print(f"Part B: {run_part_b('day9.in')}")
