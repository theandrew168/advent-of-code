from collections import defaultdict
import fileinput
import itertools

import networkx as nx


def build_graph(lines):
    G = nx.Graph()
    for line in lines:
        a, b = line.split('-')
        G.add_edge(a, b)
    return G


def part1(lines):
    graph = defaultdict(set)
    for line in lines:
        a, b = line.split('-')
        graph[a].add(b)
        graph[b].add(a)

    subs = set()
    for node, edges in graph.items():
        for a, b in itertools.combinations(edges, 2):
            if node in graph[a] and node in graph[b] and b in graph[a] and a in graph[b]:
                sub = frozenset([node, a, b])
                subs.add(sub)

    total = 0
    for sub in subs:
        if any(n[0] == 't' for n in sub):
            total += 1
    return total


def part2(lines):
    G = build_graph(lines)

    best = []
    for clique in nx.find_cliques(G):
        if len(clique) > len(best):
            best = clique
    return ','.join(sorted(best))


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
