from asyncio.log import logger
from collections import defaultdict
import enum
from json.encoder import INFINITY
from typing import Counter, List, Optional, Tuple
import logging
import sys
import itertools
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class NodeType(enum.Enum):
    FILE = 1
    DIR = 2


class Node:

    def __init__(self, name: str, type: NodeType, parent: Optional['Node']) -> None:
        self.name = name
        self.parent = parent
        self.children = set()
        self.size = 0
        self.type = type

    def __repr__(self):
        return f'Node @ {id(self)}: {self.name}, Size:{self.size}, {self.type}, Parent@{id(self.parent)},Children: {self.children}'

    def add_child(self, c: 'Node'):
        if c not in self.children:
            self.children.add(c)
            self.size += c.size

    def find_child(self, c: str):
        for n in self.children:
            if n.name == c:
                return n
        return None

    def update_size(self, old_entry, new_entry):
        self.size -= old_entry
        self.size += new_entry


class FS:

    def __init__(self) -> None:
        self.root = Node('/', NodeType.DIR, None)

    def dfs_size(self, min_size=0, max_size=INFINITY):
        res = []
        queue: List[Tuple[Node, str]] = [(self.root, '')]  # Node, tabs
        while queue:
            cur, tabs = queue.pop()
            logging.debug(f"{tabs} - {cur.name} ({cur.type}, size={cur.size})")
            if cur != self.root and cur.type == NodeType.DIR and cur.size <= max_size and cur.size >= min_size:
                res.append(cur)

            tabs += '\t'
            queue.extend([(n, tabs) for n in cur.children])

        printable = [f"{id(r)}, {r.name}, {r.size}" for r in res]
        logging.debug(f"Got dirs of len:{len(res)}: {printable}")
        return res

    def update_ls(self, cur_node: Node, ls_lines: List[str]):
        old_size = cur_node.size

        for entry in ls_lines:
            info, name = entry.split()
            if cur_node.find_child(name):
                logging.debug(
                    f"Tried to ls {name} for a second time into {cur_node.name}")
                continue
            if info == 'dir':
                new_node = Node(name, NodeType.DIR, cur_node)
            else:
                assert info.isnumeric()
                new_node = Node(name, NodeType.FILE, cur_node)
                new_node.size = int(info)

            cur_node.add_child(new_node)
        logging.debug(
            f"At {cur_node.name} Got ls with {ls_lines}\n Updated {cur_node}")

        # Update size of all parents
        temp_node = cur_node.parent
        while temp_node:
            temp_node.update_size(old_size, cur_node.size)
            temp_node = temp_node.parent

    def execute_cd(self, cur_node: Node, command_line: str) -> Node:
        new_node = None
        if command_line == '/':
            new_node = self.root
        elif command_line == '..':
            if cur_node == self.root:
                logging.debug("trying to cd .. from root")
            new_node = cur_node.parent
        else:
            # Search subdirectories
            new_node = cur_node.find_child(command_line)

        if not new_node:
            logging.debug(f"Couldnt find {command_line} in {cur_node}")

        logging.debug(
            f"At {cur_node.name} Got cd with {command_line}. Went to {new_node.name}")

        return new_node


def read_input(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        return lines


def build_fs(fp) -> FS:
    # Init
    fs = FS()
    cur_node = fs.root
    print(cur_node)

    ls_lines = []
    in_ls = False
    while True:
        l = fp.readline().strip()
        if len(l) == 0:
            if in_ls:
                fs.update_ls(cur_node, ls_lines)
            break

        if l[0] == '$':
            if in_ls:
                fs.update_ls(cur_node, ls_lines)
                ls_lines = []
                in_ls = False

            op = l[2:4]
            if op == 'cd':
                cur_node = fs.execute_cd(cur_node, l[5:])

            elif op == 'ls':
                assert in_ls == False
                assert len(ls_lines) == 0
                in_ls = True
            else:
                raise f'Got op {op}'
        else:
            assert in_ls
            ls_lines.append(l)

    return fs


def run_part_a(filename):
    fp = open(filename, 'r')
    fs = build_fs(fp)
    res = fs.dfs_size(0, 100000)
    total = sum([n.size for n in res])
    return total


def run_part_b(filename):
    fp = open(filename, 'r')
    fs = build_fs(fp)

    used = fs.root.size
    total_size = 70000000
    update_size = 30000000
    to_free = update_size - (total_size - used)

    res = fs.dfs_size(to_free, total_size)
    res_sorted = sorted(res, key=lambda x: x.size)
    to_del = res_sorted[0]
    return to_del.size


def test_part_a():
    expected = 95437
    actual = run_part_a('test7.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


def test_part_b():
    expected = 24933642
    actual = run_part_b('test7.in')

    assert actual == expected, f'{actual} and we wanted {expected}'


test_part_a()
print(f"Part A: {run_part_a('day7.in')}")

test_part_b()
print(f"Part B: {run_part_b('day7.in')}")
