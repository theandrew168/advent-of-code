from collections import defaultdict
import fileinput
from itertools import combinations, product
from pprint import pprint
import re

from more_itertools import distribute, windowed


def build_graph(lines):
    graph = defaultdict(dict)
    for line in lines:
        split = re.split(r'\s+|;|,', line)
        node, flow, edges = split[1], split[4], split[10:]
        edges = [edge for edge in edges if edge]
        flow = int(flow.split('=')[1])
        graph[node]['flow'] = flow
        graph[node]['edges'] = edges

    return graph


def bfs_dist(graph, a, b):
    v = {a: 0}
    q = [a]
    while q:
        n = q.pop(0)
        if n == b:
            break

        for e in graph[n]['edges']:
            if e in v:
                continue
            v[e] = v[n] + 1
            q.append(e)

    return v[b]


def build_clique(graph):
    nodes = [node for node in graph if graph[node]['flow'] > 0 or node == 'AA']

    clique = {}
    for a, b in product(nodes, nodes):
        if a == b:
            continue

        d = bfs_dist(graph, a, b) + 1

        # skip if seen and already shorter
        s = frozenset([a, b])
        if s in clique and clique[s] <= d:
            continue

        clique[s] = d

    return clique


def build_paths(graph, clique, path, time=0, limit=30):
    current = path[-1]
    edges = [edge for edge in clique if current in edge]
    for edge in edges:
        # isolate other node from edge
        node = set(edge) - set([current])
        node = node.pop()

        # calculate time consumed for this path
        s = frozenset([current, node])
        new_time = time + clique[s]
        if new_time >= limit:
            continue

        # add current node to path
        new_path = path + [node]
        yield new_path

        # build new clique without current node
        new_clique = {k: v for k, v in clique.items() if current not in k}

        yield from build_paths(graph, new_clique, new_path, new_time)


def pressure(graph, clique, path):
    total = 0
    rate = 0

    time = 0
    for a, b in windowed(path, 2):
        t = clique[frozenset([a, b])]
        time += t
        total += rate * t
        rate += graph[b]['flow']

    if time < 30:
        total += rate * (30 - time)

    return total


def pressure2(graph, clique, pa, pb):
    paths = []

    time = 0
    for a, b in windowed(pa, 2):
        t = clique[frozenset([a, b])]
        time += t
        paths.append((time, b))

    time = 0
    for a, b in windowed(pb, 2):
        t = clique[frozenset([a, b])]
        time += t
        paths.append((time, b))

    #print(sorted(paths))

    total = 0
    rate = 0

    time = 0
    for t, v in sorted(paths):
        if t >= 26:
            return total
        total += rate * (t - time)
        time = t
        rate += graph[v]['flow']

    if time < 26:
        total += rate * (26 - time)

    return total


def part1(lines):
    graph = build_graph(lines)
    clique = build_clique(graph)

    best = 0
    for path in build_paths(graph, clique, ['AA']):
        p = pressure(graph, clique, path)
        if p > best:
            best = p

    return best


def part2(lines):
    graph = build_graph(lines)
    clique = build_clique(graph)

    best = 0
    for path in build_paths(graph, clique, ['AA'], limit=26):
        p = pressure(graph, clique, path)
        if p > best:
            best = p

    return best


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
