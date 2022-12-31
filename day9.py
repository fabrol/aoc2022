from collections import defaultdict
from distutils.log import debug
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
    'U': +1j,
    'D': -1j,
    'R': +1,
    'L': -1
}

FOLLOW_MAP_T_MIN_H = {
    +2j: +1j,
    -2j: -1j,
    2: +1,
    -2: -1,
    -1-2j: 0-1j,
    +1-2j: 0-1j,
    -1+2j: 0+1j,
    +1+2j: 0+1j,
    +2-1j: 1+0j,
    +2+1j: 1+0j,
    -2-1j: -1+0j,
    -2+1j: -1+0j,
}


def update_T(positions: Tuple[int, int]):
    h_pos, t_pos = positions
    relative_offset = t_pos - h_pos
    if relative_offset not in FOLLOW_MAP_T_MIN_H:
        to_move = 0
    else:
        to_move = FOLLOW_MAP_T_MIN_H[relative_offset]
        t_pos = h_pos + to_move
    logging.debug(
        f"Moving {positions} using {relative_offset}:{to_move} to {(h_pos, t_pos)}")
    return (h_pos, t_pos)


def run_part_a(filename):
    movements = read_input(filename)

    # Init grid
    PositionType = Tuple[int, int]
    pos: PositionType = (0, 0)  # (H, T)
    t_visited = set()

    for m in movements:
        dir, amt = m.split()
        dir_delta = DIR_MAP[dir]
        new_pos = pos

        for _ in range(int(amt)):
            logging.debug(new_pos)
            t_visited.add(new_pos[1])

            net_new_pos = update_T((new_pos[0] + dir_delta, new_pos[1]))
            new_pos = net_new_pos

        t_visited.add(new_pos[1])
        pos = new_pos

    logging.debug(new_pos)
    return len(t_visited)


def run_part_b(filename):
    movements = read_input(filename)

    # Init grid and cache
    PositionType = Tuple[int, int]
    cache: Dict[Tuple[PositionType, Tuple[str, int]], PositionType] = {}
    pos: PositionType = (0, 0)  # (H, T)
    t_visited = set()

    for m in movements:
        dir, amt = m.split()
        dir_delta = DIR_MAP[dir]
        new_pos = pos

        # TODO: Add in use of the cache, might have to store away all t_visited along the way
        for step in range(1, int(amt)+1):
            logging.debug(new_pos)
            t_visited.add(new_pos[1])
            # Update H (Can be collapsed with call to update T)
            temp_pos = (new_pos[0] + dir_delta, new_pos[1])

            net_new_pos = update_T(temp_pos)
            new_pos = net_new_pos

        t_visited.add(new_pos[1])
        logging.debug(new_pos)
        pos = new_pos

    return len(t_visited)


def test_part_a():
    expected = 13
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
