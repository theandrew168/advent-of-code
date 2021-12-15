import fileinput
from queue import PriorityQueue


class Cave:

    def __init__(self, data, width, height):
        self.data = data
        self.width = width
        self.height = height

    def __str__(self):
        s = ''
        for y in range(self.height):
            start = y * self.width
            end = start + self.width
            row = self.data[start:end]
            s += ''.join(str(n) for n in row) + '\n'
        return s

    def get(self, x, y):
        idx = y * self.width + x
        return self.data[idx]

    def adj(self, x, y):
        for xoff in [-1, 1]:
            xx = x + xoff
            if xx < 0 or xx >= self.width:
                continue
            yield xx, y

        for yoff in [-1, 1]:
            yy = y + yoff
            if yy < 0 or yy >= self.height:
                continue
            yield x, yy

    def shortest_path(self, start_node, end_node):
        # setup costs and first point
        costs = {(x, y): None for y in range(self.width)
                              for x in range(self.height)}
        costs[start_node] = 0
    
        pq = PriorityQueue()
        pq.put((0, start_node))
    
        # iterate until all nodes have been visited
        visited = set()
        while not pq.empty():
            (dist, cur_node) = pq.get()
            visited.add(cur_node)
            for adj in cave.adj(*cur_node):
                cost = costs[cur_node] + cave.get(*adj)
                if costs[adj] is None or cost < costs[adj]:
                    pq.put((cost, adj))
                    costs[adj] = cost
    
        # reverse traverse the path
        path = []
        node = end_node
        while node != start_node:
            path.append(node)
            # follow the lowest adjacent costs
            nodes = [((x, y), costs[(x, y)]) for x, y in cave.adj(*node)]
            node = sorted(nodes, key=lambda n: n[1])[0]
            node = node[0]
    
        return reversed(path)


def part1(cave):
    start_node = (0, 0)
    end_node = (cave.width - 1, cave.height - 1)
    path = cave.shortest_path(start_node, end_node)
    return sum(cave.get(*node) for node in path)


def part2(cave):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    data = [int(n) for n in ''.join(lines)]
    width = len(lines[0])
    height = len(lines)

    cave = Cave(data, width, height)
    print(part1(cave))
    print(part2(cave))
