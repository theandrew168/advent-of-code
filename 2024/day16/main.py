from collections import deque
import fileinput
from queue import PriorityQueue

import networkx as nx


def adj4(lines, pt):
    width = len(lines[0])
    height = len(lines)
    for y in [-1, 1]:
        yield (pt[0], pt[1] + y)
    for x in [-1, 1]:
        yield (pt[0] + x, pt[1])


def shortest_path(lines, start, end):
    d = 'east'
    costs = {}
    costs[(start, d)] = 0

    pq = PriorityQueue()
    pq.put((0, start, d))

    while not pq.empty():
        cost, curr, cd = pq.get()
        for adj in adj4(lines, curr):
            ax, ay = adj
            c = lines[ay][ax]
            if c == '#':
                continue
            # calc delta on each axis
            dx, dy = ax - curr[0], ay - curr[1]
            # 180, impossible or 2001?
            if cd == 'east' and dx == -1:
                continue
            if cd == 'west' and dx == 1:
                continue
            if cd == 'south' and dy == -1:
                continue
            if cd == 'north' and dy == 1:
                continue
            new_cost = None
            new_d = None
            # same dir, cost is 1
            if cd == 'east' and dx == 1:
                new_cost = cost + 1
                new_d = cd
            elif cd == 'west' and dx == -1:
                new_cost = cost + 1
                new_d = cd
            elif cd == 'south' and dy == 1:
                new_cost = cost + 1
                new_d = cd
            elif cd == 'north' and dy == -1:
                new_cost = cost + 1
                new_d = cd
            # 90 deg turn, cost is 1001
            elif dx == 1:
                new_cost = cost + 1001
                new_d = 'east'
            elif dx == -1:
                new_cost = cost + 1001
                new_d = 'west'
            elif dy == 1:
                new_cost = cost + 1001
                new_d = 'south'
            elif dy == -1:
                new_cost = cost + 1001
                new_d = 'north'

            key = (adj, new_d)
            if key not in costs or new_cost <= costs[key]:
                costs[key] = new_cost
                pq.put((new_cost, adj, new_d))

    return costs


def build_graph(lines, start):
    width = len(lines[0])
    height = len(lines)
    start = (1, height-2, 'east')
    end = (width-2, 1)

    G = nx.Graph()
    seen = set()

    L = {
        'north': 'west',
        'west': 'south',
        'south': 'east',
        'east': 'north',
    }
    R = {
        'north': 'east',
        'east': 'south',
        'south': 'west',
        'west': 'north',
    }
    OFFS = {
        'north': (0, -1),
        'south': (0, 1),
        'east': (1, 0),
        'west': (-1, 0),
    }

    q = deque([start])
    while q:
        cx, cy, cd = q.popleft()
        if (cx, cy, cd) in seen:
            continue
        seen.add((cx, cy, cd))

        # move forward: costs 1
        ox, oy = OFFS[cd]
        ax, ay = cx + ox, cy + oy
        if lines[ay][ax] != '#':
            G.add_edge((cx, cy, cd), (ax, ay, cd), weight=1)
            q.append((ax, ay, cd))

        # turn and move left: costs 1001
        ox, oy = OFFS[L[cd]]
        ax, ay = cx + ox, cy + oy
        if lines[ay][ax] != '#':
            G.add_edge((cx, cy, cd), (ax, ay, L[cd]), weight=1001)
            q.append((ax, ay, L[cd]))

        # turn and move right: costs 1001
        ox, oy = OFFS[R[cd]]
        ax, ay = cx + ox, cy + oy
        if lines[ay][ax] != '#':
            G.add_edge((cx, cy, cd), (ax, ay, R[cd]), weight=1001)
            q.append((ax, ay, R[cd]))

    return G


def part1(lines):
    width = len(lines[0])
    height = len(lines)
    start = (1, height-2)
    end = (width-2, 1)

    costs = shortest_path(lines, start, end)
    return min(v for k,v in costs.items() if k[0] == end)


def part2(lines):
    width = len(lines[0])
    height = len(lines)

    start = (1, height-2, 'east')
    ends = [
        (width-2, 1, 'north'),
        (width-2, 1, 'east'),
    ]

    G = build_graph(lines, start)

    for end in ends:
        if end not in G:
            continue

        seen = set()
        for path in nx.all_shortest_paths(G, start, end, weight='weight'):
            s = set((pt[0], pt[1]) for pt in path)
            seen |= s
        return len(seen)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
