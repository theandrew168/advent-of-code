from collections import deque
import fileinput

import networkx as nx


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

    start = (1, height-2, 'east')
    ends = [
        (width-2, 1, 'north'),
        (width-2, 1, 'east'),
    ]

    G = build_graph(lines, start)
    best = min(nx.shortest_path_length(G, start, end, weight='weight') for end in ends if end in G)
    return best


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
