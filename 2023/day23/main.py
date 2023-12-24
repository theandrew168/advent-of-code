from collections import defaultdict
import fileinput
import queue

import sys
sys.setrecursionlimit(100000)


class Grid:
    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)

    def get(self, pt):
        x, y = pt
        return self.lines[y][x]

    def adj(self, pt):
        x, y = pt
        for xoff in [-1, 1]:
            xx = x + xoff
            if xx < 0 or xx >= self.width:
                continue
            yield (xx, y)
        for yoff in [-1, 1]:
            yy = y + yoff
            if yy < 0 or yy >= self.height:
                continue
            yield (x, yy)


def longest_path(grid, pt, seen, path, want):
    seen.add(pt)

    edges = []

    c = grid.get(pt)
    if c == '.':
        # normal tile, find adj that are not walls
        for adj in grid.adj(pt):
            if grid.get(adj) == '#':
                continue
            edges.append(adj)
    else:
        # slope tile, only adj is the slope direction
        adj = [pt[0], pt[1]]
        if c == '^':
            adj[1] -= 1
        elif c == 'v':
            adj[1] += 1
        elif c == '<':
            adj[0] -= 1
        elif c == '>':
            adj[0] += 1
        else:
            assert False
        edges.append(tuple(adj))

    scores = []
    for edge in edges:
        if edge in seen:
            continue

        new_path = path + [edge]
        if edge == want:
            return len(new_path)

        scores.append(longest_path(grid, edge, set(seen), new_path, want))

    return max(scores) if scores else 0


def nearest_nodes(grid, start):
    seen = set()
    seen.add(start)

    paths = [adj for adj in grid.adj(start) if grid.get(adj) != '#']
    for path in paths:
        node = path
        seen.add(node)

        dist = 1
        while True:
            adjs = [adj for adj in grid.adj(node) if grid.get(adj) != '#']
            adjs = [adj for adj in adjs if adj not in seen]
            if len(adjs) != 1:
                break
            adj = adjs[0]
            seen.add(adj)
            node = adj
            dist += 1
        yield node, dist


def make_graph(grid, start, end):
    edges = set()
    seen = set()

    q = queue.Queue()
    q.put(start)

    while not q.empty():
        node = q.get()
        seen.add(node)
        for adj, dist in nearest_nodes(grid, node):
            edge = (node, adj, dist)
            edges.add(edge)
            if adj in seen:
                continue

            seen.add(adj)
            q.put(adj)

    graph = defaultdict(set)
    for edge in edges:
        src, dst, cost = edge
        graph[src].add((dst, cost))
        graph[dst].add((src, cost))
    return graph


def longest_path_part2(graph, pt, seen, cost, want):
    seen.add(pt)

    edges = graph[pt]

    costs = []
    for edge in edges:
        if edge[0] in seen:
            continue

        new_cost = cost + edge[1]
        if edge[0] == want:
            return new_cost

        edge_cost = longest_path_part2(graph, edge[0], set(seen), new_cost, want)
        costs.append(edge_cost)

    return max(costs) if costs else 0


def part1(lines):
    grid = Grid(lines)
    start = (1,0)
    end = (grid.width-2, grid.height-1)
    return longest_path(grid, start, set(), [], end)


def part2(lines):
    grid = Grid(lines)
    start = (1,0)
    end = (grid.width-2, grid.height-1)

    graph = make_graph(grid, start, end)
    return longest_path_part2(graph, start, set(), 0, end)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
