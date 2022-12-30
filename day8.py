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


def run_part_b(filename):
    lines = read_input(filename)
    g = create_graph(lines)
    rows = len(g)
    cols = len(g[0])

    # [-1,-1,..] array of size 10 showing the last location in that direction for val = idx
    num_height = 10
    left = [[[-1]*num_height for _ in range(cols)] for _ in range(rows)]
    right = [
        [[cols]*num_height for _ in range(cols)] for _ in range(rows)]
    top = [[[-1]*num_height for _ in range(cols)] for _ in range(rows)]
    bottom = [[[rows]*num_height for _ in range(cols)] for _ in range(rows)]

    # Iterate over the graph 4 times, storing state for each direction each time
    # Reuse indices because we have a square grid
    for r in range(rows):
        for c in range(cols):
            # left to right
            val = g[r][c]
            if c > 0:
                left[r][c] = (left[r][c-1]).copy()
            if c > left[r][c][val]:
                left[r][c][val] = c

            # right to left
            val = g[r][cols - c - 1]
            if cols - c - 1 < cols - 1:
                right[r][cols - c - 1] = (right[r][cols - c]).copy()
            if (cols - c - 1) < right[r][cols - c - 1][val]:
                right[r][cols - c - 1][val] = cols-c-1

            # top to bottom
            val = g[c][r]
            if c > 0:
                top[c][r] = top[c-1][r].copy()
            if c > top[c][r][val]:
                top[c][r][val] = c

            # bottom to top
            val = g[cols - c - 1][r]
            if cols - c - 1 < cols - 1:
                bottom[cols-c-1][r] = bottom[cols-c][r].copy()
            if cols - c - 1 < bottom[cols-c-1][r][val]:
                bottom[cols-c-1][r][val] = cols - c - 1

    print_graph(g)
    print_graph(left)
    print_graph(right)
    print_graph(top)
    print_graph(bottom)

    res = [[-1]*cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            val = g[r][c]

            if c == 0 or r == 0 or c == cols-1 or r == rows-1:
                visible = 0
            else:
                visible = 1

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

            # top to borrom
            if r > 0:
                next_element = find_next_highest(val, top[r-1][c], True, -1)
                if not next_element:
                    next_element = 0
                visible *= (r - next_element)

            if r < rows - 1:
                next_element = find_next_highest(val, bottom[r+1][c], False, cols)
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
