import fileinput
from queue import PriorityQueue

OPP = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E',
}

OFF = {
    'N': ( 0, -1),
    'S': ( 0,  1),
    'E': ( 1,  0),
    'W': (-1,  0),
}


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


# unused, just for research
def shortest_path(grid, start, end):
    costs = {}
    costs[start] = 0

    came_from = {}
    came_from[start] = None

    pq = PriorityQueue()
    pq.put((0, start))
    while not pq.empty():
        cost, current = pq.get()

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

    start = (0, 0)
    end = (grid.width-1, grid.height-1)

    # nodes are: x, y, d, n

    costs = {}
    costs[(0, 0, None, None)] = 0

    pq = PriorityQueue()
    pq.put((0, (0, 0, None, None)))

    # iterate until all nodes have been visited
    while not pq.empty():
        cost, curr = pq.get()

        for x, y, d in grid.adj(curr[0], curr[1]):
            if curr[2] == OPP[d]:
                continue

            n = curr[3] + 1 if d == curr[2] else 1
            if n >= 4:
                continue

            adj = (x, y, d, n)
            new_cost = cost + grid.get(x, y)
            if adj not in costs or new_cost < costs[adj]:
                costs[adj] = new_cost
                pq.put((new_cost, adj))

    # lookup the best (lowest) cost
    best = None
    for k, cost in costs.items():
        if k[0] == end[0] and k[1] == end[1]:
            if best is None or cost < best:
                best = cost

    return best


def part2(lines):
    grid = Grid(lines)

    start = (0, 0)
    end = (grid.width-1, grid.height-1)

    # nodes are: x, y, d, n

    costs = {}
    costs[(0, 0, None, None)] = 0

    pq = PriorityQueue()
    pq.put((0, (0, 0, None, None)))

    # iterate until all nodes have been visited
    while not pq.empty():
        cost, curr = pq.get()

        for x, y, d in grid.adj(curr[0], curr[1]):
            if curr[2] == OPP[d]:
                continue

            n = curr[3] + 1 if d == curr[2] else 1
            if n >= 11:
                continue


            adj = (x, y, d, n)
            new_cost = cost + grid.get(x, y)

            # if not at 4 steps, jump to the spot and push
            if n < 4:
                off = OFF[d]
                px, py = x, y
                viable = True
                for _ in range(4 - n):
                    mpx, mpy = px + off[0], py + off[1]
                    if mpx < 0 or mpx >= grid.width or mpy < 0 or mpy >= grid.height:
                        viable = False
                        break
                    px, py = mpx, mpy
                    new_cost += grid.get(px, py)

                if not viable:
                    continue

                adj = (px, py, d, 4)

            if adj not in costs or new_cost < costs[adj]:
                costs[adj] = new_cost
                pq.put((new_cost, adj))

    # lookup the best (lowest) cost
    best = None
    for k, cost in costs.items():
        if k[0] == end[0] and k[1] == end[1]:
            if best is None or cost < best:
                best = cost

    return best


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
