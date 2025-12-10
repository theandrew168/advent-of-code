from collections import Counter, deque
import fileinput
import functools
import itertools
from pprint import pprint
from queue import PriorityQueue

import z3

# Would sorting the input help?
# Is this a DP problem that can be solved with a memo cache (like fib)?
# Is this a path finding problem (dijkstra's, A*, etc)?
# Is this a system of equations (z3, etc)?
# Is this a complex graph problem (networkx, etc)?


def parse(line):
    lights, *buttons, joltage = line.split()
    lights = lights[1:-1]
    buttons = [
        set(int(n) for n in button[1:-1].split(',')) for button in buttons
    ]
    joltage = tuple(int(n) for n in joltage[1:-1].split(','))
    return lights, buttons, joltage


def press1(lights, button):
    s = ''
    for i, c in enumerate(lights):
        if i in button:
            if c == '.':
                s += '#'
            else:
                s += '.'
        else:
            s += c
    return s


def solve1(dest, buttons):
    start = '.' * len(dest)

    costs = {}
    costs[start] = 0

    pq = PriorityQueue()
    pq.put((0, start))
    while not pq.empty():
        cost, lights = pq.get()
        for button in buttons:
            new_cost = cost + 1
            new_lights = press1(lights, button)
            if new_lights == dest:
                return new_cost
            if new_lights not in costs or new_cost < costs[new_lights]:
                costs[new_lights] = new_cost
                pq.put((new_cost, new_lights))


def press2(jolts, button):
    new_jolts = []
    for i, j in enumerate(jolts):
        if i in button:
            new_jolts.append(j+1)
        else:
            new_jolts.append(j)
    return tuple(new_jolts)


def dist(dest, jolts):
    dist = 0
    for i in range(len(dest)):
        diff = dest[i] - jolts[i]
        if diff < 0:
            return 999999999999
        dist += diff
    return dist


# J0123 B0   1     2   3     4     5  
# [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
# J0 = B4 + B5
# J1 = B1 + B5
# ...
# J0 = 3
# J1 = 5
# ...
# What is the sum of B0..Bn?

# [j0 == b4 + b5,
#  j1 == b1 + b5,
#  j2 == b2 + b3 + b4,
#  j3 == b0 + b1 + b3,
#  j0 == 3,
#  j1 == 5,
#  j2 == 4,
#  j3 == 7,
#  b0 >= 0,
#  b1 >= 0,
#  b2 >= 0,
#  b3 >= 0,
#  b4 >= 0,
#  b5 >= 0]

def solve2(dest, buttons):
    J = [z3.Int('j{}'.format(i)) for i in range(len(dest))]
    B = [z3.Int('b{}'.format(i)) for i in range(len(buttons))]

    equations = []
    for j in range(len(J)):
        bs = [i for i, b in enumerate(buttons) if j in b]
        equations.append(J[j] == z3.Sum(B[b] for b in bs))

    problem = []
    for i, j in enumerate(dest):
        problem.append(J[i] == j)
    for i in range(len(B)):
        problem.append(B[i] >= 0)

    total = None

    s = z3.Solver()
    s.add(equations + problem)
    while s.check() == z3.sat:
        m = s.model()
        score = sum(m[b].as_long() for b in B)
        if not total or score < total:
            total = score
        # Invalidate this solution and try again (until not sat)
        cs = [b != s.model()[b] for b in B]
        s.add(z3.Or(cs))

    return total


def part1(lines):
    total = 0
    for line in lines:
        l, b, j = parse(line)
        total += solve1(l, b)
    return total


def part2(lines):
    total = 0
    for line in lines:
        l, b, j = parse(line)
        total += solve2(j, b)
    return total


# high 15401
if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
