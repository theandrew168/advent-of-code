import fileinput
from queue import PriorityQueue

# < 1052
# < 992
# > 768


class Grid:

    def __init__(self, lines):
        self.lines = lines
        self.width = len(lines[0])
        self.height = len(lines)

    def get(self, x, y):
        return int(self.lines[y][x])

    def adj(self, x, y):
        for xx, d in [(x-1, 'W'), (x+1, 'E')]:
            if xx < 0 or xx >= self.width:
                continue
            yield xx, y, d
        for yy, d in [(y-1, 'N'), (y+1, 'S')]:
            if yy < 0 or yy >= self.height:
                continue
            yield x, yy, d


def shortest_path(grid, start, end):
    costs = {}
    costs[start] = 0

    came_from = {}
    came_from[start] = None

    pq = PriorityQueue()
    pq.put((0, start))
    while not pq.empty():
        cost, current = pq.get()
        if current == end:
            break

        for x, y, _ in grid.adj(*current):
            adj = (x, y)
            new_cost = cost + grid.get(*current)
            if adj not in costs or new_cost < costs[adj]:
                costs[adj] = new_cost
                pq.put((new_cost, adj))
                came_from[adj] = current

    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()
    return path


def part1(lines):
    grid = Grid(lines)
    path = shortest_path(grid, (0,0), (grid.width-1, grid.height-1))
    return sum(grid.get(*pt) for pt in path)

    start = (0, 0)
    costs = {(x, y, d): (None, '') for y in range(grid.height)
                                   for x in range(grid.width)
                                   for d in 'NSEW'}
    costs[(0, 0, 'E')] = (0, '')
    costs[(0, 0, 'S')] = (0, '')

    pq = PriorityQueue()
    pq.put((0, (0, 0, 'E')))
    pq.put((0, (0, 0, 'S')))

    # iterate until all nodes have been visited
    while not pq.empty():
        (dist, curr) = pq.get()
        node = costs[curr]

        # skip worse options
        if dist > costs[curr][0]:
            continue

        for x, y, d in grid.adj(curr[0], curr[1]):
            adj = (x, y, d)

            # cant go more than 3 steps in one direction
            if len(node[1]) >= 3 and node[1][-3:].count(d) >= 3:
                print('cant go this way')
                print(curr, adj, node[1], d)
                continue

            # cant reverse direction
            if node[1]:
                if node[1][-1] == 'N' and d == 'S':
                    continue
                elif node[1][-1] == 'S' and d == 'N':
                    continue
                elif node[1][-1] == 'E' and d == 'W':
                    continue
                elif node[1][-1] == 'W' and d == 'E':
                    continue

            cost = node[0] + grid.get(adj[0], adj[1])
            if costs[adj][0] is None or cost < costs[adj][0]:
                print('better way found')
                print(cost, node[1]+d)
                pq.put((cost, adj))
                costs[adj] = (cost, node[1]+d)

    for k, v in costs.items():
        if k[0] == grid.width-1 and k[1] == grid.height-1:
            print(k, v)

    return 42
#    # reverse traverse the path
#    path = []
#    node = (grid.width-1, grid.height-1)
#    while node != start:
#        path.append(node)
#
#        # follow the lowest adjacent cost
#        nodes = [((x, y), simple[(x, y)]) for x, y, _ in grid.adj(*node)]
#        node = sorted(nodes, key=lambda n: n[1])[0]
#        node = node[0]
#
#    path = list(reversed(path))
#    for p in path:
#        print(p)
#
#    return sum(grid.get(*pt) for pt in path)


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
