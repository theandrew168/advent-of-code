import fileinput
from itertools import permutations
import math


class Explode(Exception):
    pass


class Split(Exception):
    pass


class Node:

    def __init__(self, parent=None, value=None):
        self.parent = parent
        self.value = value

        self.left = None
        self.right = None

    def __str__(self):
        if self.is_number:
            return str(self.value)
        else:
            return '[{},{}]'.format(str(self.left), str(self.right))

    @property
    def magnitude(self):
        if self.is_number:
            return self.value

        return (3 * self.left.magnitude) + (2 * self.right.magnitude)

    @property
    def is_number(self):
        return self.value is not None

    @property
    def is_list(self):
        return self.value is None

    @property
    def has_parent(self):
        return self.parent is not None

    @property
    def is_left_child(self):
        if not self.has_parent:
            return False
        return self.parent.left == self

    @property
    def is_right_child(self):
        if not self.has_parent:
            return False
        return self.parent.right == self

    @property
    def left_neighbor(self):
        # search for a left subtree (node will be a right child)
        node = self
        while node.is_left_child:
            node = node.parent
            if node is None or not node.has_parent:
                return None

        # found a left subtree at this point
        node = node.parent.left

        # find the right-most child in left subtree
        while node.right:
            node = node.right

        return node

    @property
    def right_neighbor(self):
        # search for a right subtree (node will be a left child) 
        node = self
        while node.is_right_child:
            node = node.parent
            if node is None or not node.has_parent:
                return None

        # found a right subtree at this point
        node = node.parent.right

        # find the left-most child in right subtree
        while node.left:
            node = node.left

        return node


def list_to_tree(lst, parent=None):
    if isinstance(lst, int):
        return Node(parent, lst)

    n = Node(parent)
    n.left = list_to_tree(lst[0], n)
    n.right = list_to_tree(lst[1], n)

    return n


def reduce_explode(node, depth=0):
    # explode (will only be a pair of reg numbers)
    if node.is_list and depth >= 4:
        # add left to left neighbor
        left = node.left_neighbor
        if left:
            left.value = left.value + node.left.value

        # add right to right neighbor
        right = node.right_neighbor
        if right:
            right.value = right.value + node.right.value

        # replace pair with reg number 0
        zero = Node(node.parent, 0)
        if node.is_left_child:
            node.parent.left = zero
        else:
            node.parent.right = zero

        raise Explode(str(node))

    # recur
    else:
        if node.left:
            reduce_explode(node.left, depth + 1)
        if node.right:
            reduce_explode(node.right, depth + 1)


def reduce_split(node, depth=0):
    # split (only applies to nodes w/ values)
    if node.is_number and node.value >= 10:
        left = math.floor(node.value / 2)
        right = math.ceil(node.value / 2)

        pair = Node(node.parent)
        pair.left = Node(pair, left)
        pair.right = Node(pair, right)
        if node.is_left_child:
            node.parent.left = pair
        else:
            node.parent.right = pair

        raise Split(str(node))

    # recur
    else:
        if node.left:
            reduce_split(node.left, depth + 1)
        if node.right:
            reduce_split(node.right, depth + 1)


def settle(node):
    # reduce until the number settles
    while True:
        try:
            reduce_explode(node)
            reduce_split(node)
        except Explode as e:
            continue
        except Split as e:
            continue
        else:
            break


def add(a, b):
    node = Node()

    node.left = a
    node.right = b
    node.left.parent = node
    node.right.parent = node

    settle(node)
    return node


def part1(lines):
    nodes = []
    for line in lines:
        node = list_to_tree(eval(line))
        nodes.append(node)

    answer = nodes[0]
    for node in nodes[1:]:
        answer = add(answer, node)

    return answer.magnitude


def part2(lines):
    answer = 0
    for a, b in permutations(range(len(lines)), 2):
        na = list_to_tree(eval(lines[a]))
        nb = list_to_tree(eval(lines[b]))
        s = add(na, nb)
        m = s.magnitude
        if m > answer:
            answer = m
    return answer


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
