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
    0: 0,
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
    #relative_offset = t_pos - h_pos
    delta = follow_map_delta(h_pos, t_pos)
    '''
    if relative_offset not in FOLLOW_MAP_T_MIN_H:
        to_move = 0
    else:
        to_move = FOLLOW_MAP_T_MIN_H[relative_offset]
        t_pos = h_pos + to_move
    '''
    t_pos = t_pos + delta
    # logging.debug(
    #    f"Moving {delta} from {h_pos},{positions[1]}:{t_pos}")
    # logging.debug(
    #    f"Moving {positions} using {relative_offset}:{to_move} to {(h_pos, t_pos)}")
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


def move_knots(pos: List, dir, amt, cache, visited):
    new_pos = pos.copy()
    logging.debug(f"Moving {dir}:{amt}")
    while amt > 0:
        '''
        source = (new_pos, dir)
        if source not in cache:
            cache[source] = []
        jump = None

        # Replect with bisect and sorted array
        for (dist, nnp) in sorted(cache[source], reverse=True):
            if dist <= amt:
                jump = (dist, nnp)
                #hits += 1
                break
        '''

        jump = False
        if jump:
            # We have a jump in the cache
            logging.debug(f"Trying to jump {jump} {source}")
            new_pos = jump[1]
            amt -= jump[0]
        else:
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
            #cache[source].append((amt, net_new_pos))
            amt = 0

    # logging.debug(rope_str(new_pos))
    return new_pos


def move_head_tail_pair(head_pos, tail_pos, dir, amt, cache, visited):
    new_pos = (head_pos, tail_pos)
    while amt > 0:
        source = (new_pos, dir)
        if source not in cache:
            cache[source] = []
        jump = None

        # Replect with bisect and sorted array
        for (dist, nnp) in sorted(cache[source], reverse=True):
            if dist <= amt:
                jump = (dist, nnp)
                #hits += 1
                break

        if jump:
            # We have a jump in the cache
            logging.debug(f"Trying to jump {jump} {source}")
            new_pos = jump[1]
            amt -= jump[0]
        else:
            for _ in range(int(amt)):
                logging.debug(new_pos)
                visited.add(new_pos[1])

                net_new_pos = update_T(
                    (new_pos[0] + DIR_MAP[dir], new_pos[1]))
                new_pos = net_new_pos
            cache[source].append((amt, net_new_pos))
            amt = 0

    return new_pos


def run_part_b(filename):
    movements = read_input(filename)

    # Init grid and cache
    PositionsType = Tuple[int, int]
    pos: PositionsType = [0]*10  # (H, 1,2,...9)
    t_visited = set()
    hits = None

    # (Abs pos, dir) -> [(amt, final_pos)] (Only for knot over knot repeats. can go further and make cache for relative positions)
    cache: Dict[Tuple[PositionsType, Tuple[str, int]],
                PositionsType] = {}

    for m in movements:
        dir, amt = m.split()
        net_amt = int(amt)
        dir_delta = DIR_MAP[dir]
        # for knot_i in range(0, len(pos)-1, 1):
        #    lagging_pos = (new_pos[knot_i], pos[knot_i+1])
        #    amt = net_amt

        new_pos = move_knots(
            pos, dir, int(amt), cache, t_visited)
        # new_pos = move_head_tail_pair(
        #    pos[0], pos[1], dir, int(amt), cache, t_visited)

        t_visited.add(new_pos[-1])
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
    logging.debug("Starting test b")
    expected = 36
    actual = run_part_b('test9b.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


'''
test_part_a()
print(f"Part A: {run_part_a('day9.in')}")
'''
test_part_b()
print(f"Part B: {run_part_b('day9.in')}")
