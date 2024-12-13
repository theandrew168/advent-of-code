import fileinput
import math
from queue import PriorityQueue

import z3


def parse(lines):
    m = {}
    for line in lines:
        if not line:
            yield m
            m = {}
            continue

        fields = line.split()
        if fields[1] == 'A:':
            x, y = fields[2][2:-1], fields[3][2:]
            x, y = int(x), int(y)
            m['a'] = (x, y)
        elif fields[1] == 'B:':
            x, y = fields[2][2:-1], fields[3][2:]
            x, y = int(x), int(y)
            m['b'] = (x, y)
        else:
            x, y = fields[1][2:-1], fields[2][2:]
            x, y = int(x), int(y)
            m['p'] = (x, y)

    yield m


def shortest_path(options, start, end):
    costs = {}
    costs[start] = 0

    pq = PriorityQueue()
    pq.put((0, start))
    while not pq.empty():
        cost, curr = pq.get()
        for tokens, (x, y) in options:
            adj = (curr[0]+x, curr[1]+y)
            # stop if we've overshot the prize
            if adj[0] > end[0] or adj[1] > end[1]:
                continue
            new_cost = cost + tokens
            if adj not in costs or new_cost < costs[adj]:
                costs[adj] = new_cost
                pq.put((new_cost, adj))

    return costs


def part1(lines):
    machines = list(parse(lines))

    total = 0
    for m in machines:
        options = [(3, m['a']), (1, m['b'])]
        start = (0, 0)
        end = m['p']
        costs = shortest_path(options, start, end)
        total += costs[end] if end in costs else 0
    return total


def part2(lines):
    machines = list(parse(lines))

    total = 0
    for m in machines:
        a, b = z3.Ints('a b')
        ax, bx, ay, by = z3.Ints('ax bx ay by')
        px, py = z3.Ints('px py')

        equations = [
            a * ax + b * bx == px,
            a * ay + b * by == py,
        ]

        problem = [
            ax == m['a'][0],
            ay == m['a'][1],
            bx == m['b'][0],
            by == m['b'][1],
            px == m['p'][0] + 10000000000000,
            py == m['p'][1] + 10000000000000,
        ]

        s = z3.Solver()
        s.add(equations + problem)
        s.check()

        try:
            m = s.model()
            total += m[a].as_long() * 3 + m[b].as_long()
        except:
            continue

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
