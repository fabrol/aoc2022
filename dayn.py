from collections import defaultdict
from typing import Counter, List, Tuple
import logging
import sys
import itertools
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def run_part_a(filename):
    fp = open(filename, 'r')
    for l in fp.readlines():
        l = l.strip()
    pass


def run_part_b(filename):
    fp = open(filename, 'r')
    pass


def test_part_a():
    expected = 5353
    actual = run_part_a('test8.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


def test_part_b():
    expected = 5353
    actual = run_part_b('test8.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


test_part_a()
print(f"Part A: {run_part_a('day8.in')}")

test_part_b()
print(f"Part B: {run_part_b('day8.in')}")
