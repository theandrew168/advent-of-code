from collections import defaultdict, deque
import copy
import fileinput
from queue import PriorityQueue


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

    came_from = defaultdict(set)

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
            # 90 deg turn, cost is 1000
            elif dx == 1:
                adj = curr
                new_cost = cost + 1000
                new_d = 'east'
            elif dx == -1:
                adj = curr
                new_cost = cost + 1000
                new_d = 'west'
            elif dy == 1:
                adj = curr
                new_cost = cost + 1000
                new_d = 'south'
            elif dy == -1:
                adj = curr
                new_cost = cost + 1000
                new_d = 'north'

            key = (adj, new_d)
            if key not in costs or new_cost <= costs[key]:
                costs[key] = new_cost
                pq.put((new_cost, adj, new_d))
                came_from[adj].add((curr, cd))

    return costs, came_from


def part1(lines):
    width = len(lines[0])
    height = len(lines)
    start = (1, height-2)
    end = (width-2, 1)

    costs, _ = shortest_path(lines, start, end)
    return min(v for k,v in costs.items() if k[0] == end)


def calc_cost(a, b):
    if a == b:
        return 1000
    return 1


def part2(lines):
    width = len(lines[0])
    height = len(lines)
    start = (1, height-2)
    end = (width-2, 1)

    flip = {
        'east': 'west',
        'west': 'east',
        'north': 'south',
        'south': 'north',
    }

    costs, came_from = shortest_path(lines, start, end)
    best = min(v for k,v in costs.items() if k[0] == end)
    

#    import pprint
#    pprint.pprint(came_from)
#    pprint.pprint(came_from[(5,7)])
#    return

    tiles = set([end])

    q = deque()
    q.append((end, best))
    while q:
        curr, score = q.popleft()
        for adj, d in came_from[curr]:
            new_score = score - calc_score(curr, adj)
            key = (adj, d)
            prev_cost = costs[key]
            cost = calc_cost(adj, curr, )
            if prev_cost + cost == costs[(curr, d)]:
                print('{} -> {} going {} on path'.format(adj, curr, d))
                tiles.add(adj)
                q.append(adj)

    print(tiles)
    return len(tiles)


# 509 too low
if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
