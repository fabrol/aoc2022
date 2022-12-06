from collections import Counter
from typing import Counter, List, Tuple
import logging
import sys
import itertools
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def read_input(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def run_part_a(filename, m_length):
    fp = open(filename, 'r')
    res = []
    while True:
        l = fp.readline().strip()
        if not l:
            return res

        buffer = Counter(l[0:m_length])
        for i in range(m_length, len(l)):
            if len(buffer.keys()) == m_length:
                res.append(i)
                break
            buffer[l[i-m_length]] -= 1
            if buffer[l[i-m_length]] == 0:
                del buffer[l[i-m_length]]
            buffer[l[i]] += 1


def run_part_b(filename):
    fp = open(filename, 'r')
    pass


def test_part_a():
    expected = [7, 5, 6, 10, 11]
    actual = run_part_a('test6.in', 4)

    assert actual == expected, f'{actual} and we wanted {expected}'


def test_part_b():
    expected = [19, 23, 23, 29, 26]
    actual = run_part_a('test6.in', 14)

    assert actual == expected, f'{actual} and we wanted {expected}'


test_part_a()
print(f"Part A: {run_part_a('day6.in', 4)}")

test_part_b()
print(f"Part B: {run_part_a('day6.in', 14)}")
