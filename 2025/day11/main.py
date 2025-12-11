from collections import Counter, defaultdict, deque
import fileinput
import functools
import itertools
from pprint import pprint
from queue import PriorityQueue

# Would sorting the input help?
# Is this a DP problem that can be solved with a memo cache (like fib)?
# Is this a path finding problem (dijkstra's, A*, etc)?
# Is this a system of equations (z3, etc)?
# Is this a complex graph problem (networkx, etc)?


def parse(lines):
    graph = defaultdict(list)
    for line in lines:
        k, *vs = line.split()
        k = k[:-1]
        graph[k].extend(vs)
    return graph


def invert(graph):
    inverted = defaultdict(list)
    for n, es in graph.items():
        for e in es:
            inverted[e].append(n)
    return inverted


def count_paths(graph, start, end):
    inverted = invert(graph)

    # top-down (memo) DP
    @functools.cache
    def paths_from(a, b):
        if a == b:
            return 1
        return sum(paths_from(a, e) for e in inverted[b])

    return paths_from(start, end)


def part1(lines):
    graph = parse(lines)
    return count_paths(graph, 'you', 'out')


def part2(lines):
    graph = parse(lines)

    a = 1
    A = ['svr', 'dac', 'fft', 'out']
    for i in range(len(A) - 1):
        start, end = A[i], A[i+1]
        score = count_paths(graph, start, end)
        a *= score

    b = 1
    B = ['svr', 'fft', 'dac', 'out']
    for i in range(len(B) - 1):
        start, end = B[i], B[i+1]
        score = count_paths(graph, start, end)
        b *= score

    return a + b


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
