from collections import defaultdict, deque
import copy
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

    # track all paths that lead to an (x,y) key
    paths = defaultdict(list)
    paths[start] = [[start]]

    pq = PriorityQueue()
    pq.put((0, start, d))

    while not pq.empty():
        cost, curr, cd = pq.get()
        if cost > costs[(curr, cd)]:
            continue

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

            key = (curr, cd)
            if key not in costs or new_cost <= costs[key]:
                # we just found an equiv or better path to this point
                # its path is ANY path to curr + adj
                # if the path is strictly better, we should dump the old paths
                # each path to curr is also now a path to curr + adj
                # add each of these new paths to adj (if not there already)

                # if a better path was found, reset paths to this point
                if key not in costs:
                    costs[key] = new_cost
                elif new_cost < costs[key]:
                    costs[key] = new_cost
                    paths[adj] = []

                # note all paths to the prev point
                paths_to_curr = paths[curr]

                # for each one...
                for path in paths_to_curr:
                    # construct a new path to the adj point
                    path_to_adj = path + [adj]
                    # add to the list of paths to adj (if it is new)
                    if path_to_adj not in paths[adj]:
                        paths[adj].append(path_to_adj)

                pq.put((new_cost, adj, new_d))

    return costs, paths


def part1(lines):
    width = len(lines[0])
    height = len(lines)
    start = (1, height-2)
    end = (width-2, 1)

    costs, _ = shortest_path(lines, start, end)
    return min(v for k,v in costs.items() if k[0] == end)


def part2(lines):
    width = len(lines[0])
    height = len(lines)
    start = (1, height-2)
    end = (width-2, 1)

    G = nx.Graph()

    seen = set()
    q = deque([(start, 'east')])
    while q:
        curr, cd = q.popleft()
        if (curr, cd) in seen:
            continue
        seen.add((curr,cd))
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

            # same dir, cost is 1
            if cd == 'east' and dx == 1:
                G.add_edge(curr, adj, weight=1)
                q.append((adj, cd))
            elif cd == 'west' and dx == -1:
                G.add_edge(curr, adj, weight=1)
                q.append((adj, cd))
            elif cd == 'south' and dy == 1:
                G.add_edge(curr, adj, weight=1)
                q.append((adj, cd))
            elif cd == 'north' and dy == -1:
                G.add_edge(curr, adj, weight=1)
                q.append((adj, cd))
            # 90 deg turn, cost is 1001
            elif dx == 1:
                G.add_edge(curr, adj, weight=1001)
                q.append((adj, 'east'))
            elif dx == -1:
                G.add_edge(curr, adj, weight=1001)
                q.append((adj, 'west'))
            elif dy == 1:
                G.add_edge(curr, adj, weight=1001)
                q.append((adj, 'south'))
            elif dy == -1:
                G.add_edge(curr, adj, weight=1001)
                q.append((adj, 'north'))

    seen = set()
    for path in nx.all_shortest_paths(G, start, end):
        for p in path:
            print(p)
            seen.add(p)
    return len(seen)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    #print(part1(lines))
    print(part2(lines))
