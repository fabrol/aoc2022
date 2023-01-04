from distutils.log import debug
import pprint
from re import S
from typing import Counter, DefaultDict, Dict, List, Tuple
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
    # logging.debug(
    #    f"Moving {positions} using {relative_offset}:{to_move} to {(h_pos, t_pos)}")
    return (h_pos, t_pos)


def run_part_a(filename):
    movements = read_input(filename)

    # Init grid
    pos= (0, 0)  # (H, T)
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
    pos = (0,0)
    
    PositionsType = Tuple[int, int]
    #pos: PositionType = [(0)]*10  # (H, 1,2,...9)
    t_visited = set()
    # Relative pos(t - h), (dir, amt) -> Relative pos
    cache: Dict[Tuple[PositionsType, Tuple[str, int]],
                PositionsType] = {}

    hits = 0
    for m in movements:
        dir, amt = m.split()
        amt = int(amt)
        dir_delta = DIR_MAP[dir]
        new_pos = pos

        # pos A, Dir, 10 -> check for any amount < amt in dir and move by that much. if none, move by 1
        while amt > 0:
            source = (new_pos, dir)
            if source not in cache:
                cache[source] = []
            jump = None

            # Replect with bisect and sorted array
            for (dist, nnp) in sorted(cache[source], reverse=True):
                if dist <= amt:
                    jump = (dist, nnp)
                    hits += 1
                    break

            if jump:
                # We have a jump in the cache
                logging.debug(f"Trying to jump {jump} {source}")
                new_pos = jump[1]
                amt -= jump[0]
            else:
                for _ in range(int(amt)):
                    logging.debug(new_pos)
                    t_visited.add(new_pos[1])

                    net_new_pos = update_T(
                        (new_pos[0] + dir_delta, new_pos[1]))
                    new_pos = net_new_pos
                cache[source].append((amt, net_new_pos))
                amt = 0

        t_visited.add(new_pos[1])
        pos = new_pos

    logging.debug(new_pos)
    # logging.debug(pprint.pformat(cache))
    logging.debug(f"Size of cache:{len(cache)}, Hits:{hits}")
    return len(t_visited)


def test_part_a():
    expected = 13
    actual = run_part_a('test9.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


def test_part_b():
    expected = 13
    actual = run_part_b('test9.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


'''
test_part_a()
print(f"Part A: {run_part_a('day9.in')}")
'''
test_part_b()
print(f"Part B: {run_part_b('day9.in')}")
