from audioop import reverse
from collections import defaultdict
import re
from typing import Counter, List, Tuple
import logging
import sys
import itertools
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def run_part_a(filename, reverse = True):
    fp = open(filename, 'r')
    stacks = []

    while True:
        l = fp.readline()
        if l == "\n":
            break

        l = l[:-1]
        for stack_offset in range(0, len(l), 4):
            stack = l[stack_offset+1:stack_offset+2]

            if stack.isdigit():
                continue

            stack_i = int(stack_offset/4)
            if (stack_i) >= len(stacks):
                stacks.append([])

            if stack != ' ':
                stacks[stack_i].append(stack)

    stacks = [list(reversed(s)) for s in stacks]
    logging.debug(stacks)

    # Time for moves
    while True:
        l = fp.readline().strip()
        if len(l) == 0:
            break

        amt, frm, to = list(
            map(int, re.match('move (\d+) from (\d+) to (\d+)', l).groups()))
        frm -= 1
        to -= 1
        if reverse:
            stacks[to].extend(list(reversed(stacks[frm][-amt:])))
        else:
            stacks[to].extend(stacks[frm][-amt:])
        stacks[frm] = stacks[frm][:-amt]
        #logging.debug(f"Moving {amt} {frm}:{to} Ending up with {stacks}")

    output = [s[-1] for s in stacks]
    logging.debug(stacks)
    return ''.join(output)


def run_part_b(filename):
    fp = open(filename, 'r')
    pass


def test_part_a():
    expected = 'CMZ'
    actual = run_part_a('test5.in', True)

    assert actual == expected, f'{actual} and we wanted {expected}'


def test_part_b():
    expected = 'MCD'
    actual = run_part_a('test5.in', False)

    assert actual == expected, f'{actual} and we wanted {expected}'


test_part_a()
print(f"Part A: {run_part_a('day5.in')}")

test_part_b()
print(f"Part B: {run_part_a('day5.in', False)}")
