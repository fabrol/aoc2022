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
    lines = [l.strip() for l in fp.readlines()]
    res = []
    for l in lines:
        size = len(l)
        assert size % 2 == 0
        left, right = set(l[:int(size/2)]), set(l[int(size/2):])
        val = list(left.intersection(right))
        assert len(val) == 1
        conv = ord(val[0]) - \
            96 if val[0].islower() else (ord(val[0]) - 65 + 27)
        #print(f"{val[0]} : {conv}")
        res.append(conv)

    return sum(res)


def run_part_b(filename):
    fp = open(filename, 'r')
    lines = [l.strip() for l in fp.readlines()]
    final = []
    for i in range(0, len(lines), 3):
        packs = lines[i:i+3]
        res = set()
        for p in packs:
            res = set(p) if len(res) == 0 else res.intersection(set(p))
        val = list(res)[0]
        conv = ord(val[0]) - \
            96 if val[0].islower() else (ord(val[0]) - 65 + 27)
        #print(f"{val[0]} : {conv}")
        final.append(conv)
    return sum(final)


def test_part_a():
    expected = 157
    actual = run_part_a('test3.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


def test_part_b():
    expected = 70
    actual = run_part_b('test3.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


test_part_a()
print(f"Part A: {run_part_a('day3.in')}")

test_part_b()
print(f"Part B: {run_part_b('day3.in')}")
