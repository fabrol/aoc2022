from collections import defaultdict
from typing import Counter, List, OrderedDict, Tuple
import logging
import sys
import itertools
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def who_wins(a, b):
    diff = abs(a-b)
    if diff == 0:
        res = -1
    elif diff > 1:
        res = 1 if a > b else 0
    else:
        res = 1 if a < b else 0
    return res


CONV_ = {
    'A': 1,
    'B': 2,
    'C': 3,
    'X': 1,
    'Y': 2,
    'Z': 3,
}

WIN_CONV_ = {
    -1: 3,
    0: 0,
    1: 6
}

CONV_OUTCOMES_ = {
    'X': (0, 0),
    'Y': (1, 3),
    'Z': (2, 6),
}

# val: score of choice, row (opp) : R,P,S col (target): L, D, W
STRAT = [
    [3, 1, 2],
    [1, 2, 3],
    [2, 3, 1]
]


def calc_score(line):
    opp, you = tuple(map(lambda x: CONV_[x], line.split()))
    return you + WIN_CONV_[who_wins(opp, you)]


def calc_score_b(line):
    opp, target = line.split()
    you_play_score = STRAT[CONV_[opp]-1][CONV_OUTCOMES_[target][0]]

    return CONV_OUTCOMES_[target][1] + you_play_score


def run_part_a(filename):
    fp = open(filename, 'r')
    score = 0
    for l in fp.readlines():
        score += calc_score(l.strip())
    return score


def run_part_b(filename):
    fp = open(filename, 'r')
    score = 0
    for l in fp.readlines():
        score += calc_score_b(l.strip())
    return score


def test_part_a():
    expected = 15
    actual = run_part_a('test2.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


def test_part_b():
    expected = 12
    actual = run_part_b('test2.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


test_part_a()
print(f"Part A: {run_part_a('day2.in')}")

test_part_b()
print(f"Part B: {run_part_b('day2.in')}")
