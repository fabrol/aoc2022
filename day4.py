from collections import defaultdict
from typing import Counter, List, Tuple
import logging
import sys
import itertools
import re
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def run_part_a(filename):
    fp = open(filename, 'r')
    res = 0
    while True:
        l = fp.readline().strip()
        if not l:
            break
        l1, r1, l2, r2 = list(
            map(int, re.match('(\d+)-(\d+),(\d+)-(\d+)', l).groups()))

        if (l1 >= l2 and r1 <= r2) or (l2 >= l1 and r2 <= r1):
            logging.debug(f"Adding {l}: {l1}:{r1} {l2}:{r2}")
            res += 1
    return res


def run_part_b(filename):
    fp = open(filename, 'r')
    res = 0
    total = 0
    while True:
        l = fp.readline().strip()
        if not l:
            break
        total += 1
        l1, r1, l2, r2 = list(
            map(int, re.match('(\d+)-(\d+),(\d+)-(\d+)', l).groups()))

        if (l1 > r2) or (l2 > r1):
            logging.debug(f"Adding {l}: {l1}:{r1} {l2}:{r2}")
            res += 1
    return (total - res)


def test_part_a():
    expected = 2
    actual = run_part_a('test4.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


def test_part_b():
    expected = 4
    actual = run_part_b('test4.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


test_part_a()
print(f"Part A: {run_part_a('day4.in')}")

test_part_b()
print(f"Part B: {run_part_b('day4.in')}")
