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

FOLLOW_MAP_DYNAMIC = {
    0: 0
}


def follow_map_delta(h_pos, t_pos):
    delta = h_pos - t_pos

    if delta in FOLLOW_MAP_DYNAMIC:
        return FOLLOW_MAP_DYNAMIC[delta]

    if abs(delta) < 2:
        FOLLOW_MAP_DYNAMIC[delta] = 0
        return 0

    if delta.real == 0 or delta.imag == 0:
        res = (delta / abs(delta))
        FOLLOW_MAP_DYNAMIC[delta] = res
        return res

    if abs(delta) >= 2:
        delta_x = h_pos.real - t_pos.real
        delta_y = h_pos.imag - t_pos.imag
        res = complex((delta_x / abs(delta_x)), (delta_y / abs(delta_y)))
        FOLLOW_MAP_DYNAMIC[delta] = res
        return res

    assert False, f"WTF got {delta} with {h_pos}{t_pos}"


def update_T(positions: Tuple[int, int]):
    h_pos, t_pos = positions
    delta = follow_map_delta(h_pos, t_pos)
    t_pos = t_pos + delta
    # logging.debug(
    #    f"Moving {delta} from {h_pos},{positions[1]}:{t_pos}")
    return (h_pos, t_pos)


def run_part_a(filename):
    movements = read_input(filename)

    # Init grid
    pos = (0, 0)  # (H, T)
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


def rope_str(rope_arr, max_x=None, max_y=None):
    if not max_x:
        max_x = max([abs(int(x.real)) for x in rope_arr]) + 1
    if not max_y:
        max_y = max([abs(int(x.imag)) for x in rope_arr]) + 1
    limits = max(max_x, max_y)

    res_str = '\n'
    for y in range(limits, -limits, -1):
        for x in range(-limits, limits, 1):
            point = complex(x, y)
            if point in rope_arr:
                idx = rope_arr.index(point)
                res_str += str(idx)
            else:
                res_str += '.'
        res_str += '\n'

    return res_str


def move_knots(pos: List, dir, amt, visited):
    new_pos = pos.copy()
    logging.debug(f"Moving {dir}:{amt}")
    for step in range(int(amt)):
        #logging.debug(f"Step {step} with {new_pos}")
        # logging.debug(rope_str(new_pos))
        visited.add(new_pos[-1])

        new_head = update_T(
            (new_pos[0] + DIR_MAP[dir], new_pos[1]))
        new_pos[0] = new_head[0]
        new_pos[1] = new_head[1]

        for i in range(1, len(pos)-1):
            # logging.debug(
            #    f"Inner step {i} with {rope_str(new_pos, 7,7)}")
            _, new_t = update_T(
                (new_pos[i], new_pos[i+1]))
            new_pos[i+1] = new_t

    # logging.debug(rope_str(new_pos))
    return new_pos


def run_part_b(filename):
    movements = read_input(filename)

    # Init grid and cache
    PositionsType = Tuple[int, int]
    pos: PositionsType = [0]*10  # (H, 1,2,...9)
    t_visited = set()

    for m in movements:
        dir, amt = m.split()
        new_pos = move_knots(
            pos, dir, int(amt), t_visited)

        t_visited.add(new_pos[-1])
        pos = new_pos

    logging.debug(new_pos)
    return len(t_visited)


def test_part_a():
    expected = 13
    actual = run_part_a('test9.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


def test_part_b():
    logging.debug("Starting test b")
    expected = 36
    actual = run_part_b('test9b.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


test_part_a()
print(f"Part A: {run_part_a('day9.in')}")

test_part_b()
print(f"Part B: {run_part_b('day9.in')}")
