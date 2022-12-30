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


def create_graph(lines):
    grid = []
    for l in lines:
        grid.append([int(x) for x in l])
    return grid


def print_graph(grid, visible=None):
    for row in range(len(grid)):
        s = ""
        for col in range(len(grid[0])):
            if visible and (row, col) in visible:
                s += f"\x1b[31;20m{grid[row][col]:2d}\x1b[0m, "
            else:
                if type(grid[row][col]) == list:
                    res = ', '.join(f"{x:2d}" for x in grid[row][col])
                    s += '[' + res + ']'
                else:
                    s += f"{grid[row][col]:2d}, "
        logging.debug(s)
    logging.debug('\n')


def run_part_a(filename):
    lines = read_input(filename)
    g = create_graph(lines)
    rows = len(g)
    cols = len(g[0])

    top = [[-1]*cols for _ in range(rows)]
    left = [[-1]*cols for _ in range(rows)]
    right = [[-1]*cols for _ in range(rows)]
    bottom = [[-1]*cols for _ in range(rows)]

    # Iterate over the graph 4 times, storing state for each direction each time
    # Reuse indices because we have a square grid
    for r in range(rows):
        cur_max_left = -1
        cur_max_right = -1
        cur_max_top = -1
        cur_max_bottom = -1
        for c in range(cols):
            # left to right
            val = g[r][c]
            if val > cur_max_left:
                cur_max_left = val
            left[r][c] = cur_max_left

            # right to left
            val = g[r][cols - c - 1]
            if val > cur_max_right:
                cur_max_right = val
            right[r][cols - c - 1] = cur_max_right

            # top to bottom
            val = g[c][r]
            if val > cur_max_top:
                cur_max_top = val
            top[c][r] = cur_max_top

            # top to bottom
            val = g[cols - c - 1][r]
            if val > cur_max_bottom:
                cur_max_bottom = val
            bottom[cols - c - 1][r] = cur_max_bottom

    visible = []
    for r in range(rows):
        for c in range(cols):
            if r == 0 or c == 0 or r == rows-1 or c == cols-1:
                visible += [(r, c)]
            else:
                val = g[r][c]
                if val > left[r][c-1] or val > right[r][c+1] or val > top[r-1][c] or val > bottom[r+1][c]:
                    visible += [(r, c)]

    '''
    print_graph(g)
    print_graph(left)
    print_graph(right)
    print_graph(top)
    print_graph(bottom)
    '''
    print_graph(g, visible)
    return len(visible)


"""
Goal: Find the closest height h >= current in the scan direction with only heights <= h between h and current
forward_pass = starting from index 0 and going to max, false = starting from max index
"""


def find_next_highest(val, next_array, forward_pass, default_val, max_height=10):
    next_so_far = None
    for ht in range(val, max_height):
        if next_array[ht] != default_val:
            if next_so_far == None:
                next_so_far = next_array[ht]
            else:
                if forward_pass:
                    next_so_far = max(next_so_far, next_array[ht])
                else:
                    next_so_far = min(next_so_far, next_array[ht])
    return next_so_far


def init_arrays(rows, cols, num_height, init_val):
    return [[[init_val]*num_height for _ in range(cols)] for _ in range(rows)]


def run_part_b(filename):
    lines = read_input(filename)
    g = create_graph(lines)
    rows = len(g)
    cols = len(g[0])
    size = cols

    # [-1,-1,..] array of size 10 showing the last location in that direction for val = idx
    num_height = 10
    left = init_arrays(rows, cols, num_height, -1)
    right = init_arrays(rows, cols, num_height, cols)
    top = init_arrays(rows, cols, num_height, -1)
    bottom = init_arrays(rows, cols, num_height, rows)

    # Iterate over the graph 4 times, storing state for each direction each time
    # This is storing away the next closest location from scan direction of each height
    for major in range(size):
        for minor in range(size):
            # left to right
            mr, mi = major, minor  # Major, minor
            val = g[mr][mi]
            if mi > 0:
                left[mr][mi] = (left[mr][mi-1]).copy()
            if mi > left[mr][mi][val]:
                left[mr][mi][val] = mi

            # right to left
            mr, mi = major, size-1-minor
            val = g[mr][mi]
            if mi < size - 1:
                right[mr][mi] = (right[mr][mi+1]).copy()
            if mi < right[mr][mi][val]:
                right[mr][mi][val] = mi

            # top to bottom
            mr, mi = minor, major
            val = g[mr][mi]
            if mr > 0:
                top[mr][mi] = top[mr-1][mi].copy()
            if mr > top[mr][mi][val]:
                top[mr][mi][val] = mr

            # bottom to top
            mr, mi = size-1-minor, major
            val = g[mr][mi]
            if mr < size - 1:
                bottom[mr][mi] = bottom[mr+1][mi].copy()
            if mr < bottom[mr][mi][val]:
                bottom[mr][mi][val] = mr

    '''
    print_graph(g)
    print_graph(left)
    print_graph(right)
    print_graph(top)
    print_graph(bottom)
    '''

    res = [[-1]*cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            val = g[r][c]

            if c == 0 or r == 0 or c == cols-1 or r == rows-1:
                visible = 0
            else:
                visible = 1

            # Left to right
            if c > 0:
                next_element = find_next_highest(val, left[r][c-1], True, -1)
                if not next_element:
                    next_element = 0
                visible *= (c - next_element)

            # Right to left
            if c < cols - 1:
                next_element = find_next_highest(
                    val, right[r][c+1], False, cols)

                if not next_element:
                    next_element = cols - 1
                visible *= (next_element - (c))

            # top to bottom
            if r > 0:
                next_element = find_next_highest(val, top[r-1][c], True, -1)
                if not next_element:
                    next_element = 0
                visible *= (r - next_element)

            # bottom to top
            if r < rows - 1:
                next_element = find_next_highest(
                    val, bottom[r+1][c], False, rows)
                if not next_element:
                    next_element = rows - 1
                visible *= (next_element - r)

            res[r][c] = visible

    print_graph(res)
    return max([max(r) for r in res])


def test_part_a():
    expected = 21
    actual = run_part_a('test8.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


def test_part_b():
    expected = 8
    actual = run_part_b('test8.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


test_part_a()
print(f"Part A: {run_part_a('day8.in')}")

test_part_b()
print(f"Part B: {run_part_b('day8.in')}")
