import fileinput
from queue import PriorityQueue


def parse(lines):
    for line in lines:
        x, y = line.split(',')
        x, y = int(x), int(y)
        yield (x, y)


def adj4(pt):
    x, y = pt
    return [
        (x+1, y),
        (x-1, y),
        (x, y+1),
        (x, y-1),
    ]


def shortest_path(width, height, bad, start, end):
    costs = {}
    costs[start] = 0

    pq = PriorityQueue()
    pq.put((0, start))
    while not pq.empty():
        cost, curr = pq.get()
        for adj in adj4(curr):
            x, y = adj
            if x < 0 or x >= width:
                continue
            if y < 0 or y >= height:
                continue 
            if adj in bad:
                continue

            new_cost = cost + 1
            if adj not in costs or new_cost < costs[adj]:
                costs[adj] = new_cost
                pq.put((new_cost, adj))

    return costs


def part1(lines):
    width = 71
    height = 71

    start = (0, 0)
    end = (width-1, height-1)

    bad = set(parse(lines[:1024]))
    costs = shortest_path(width, height, bad, start, end)
    return costs[end]


def part2(lines):
    width = 71
    height = 71
    limit = 1024
    #width = 7
    #height = 7
    #limit = 12
    

    start = (0, 0)
    end = (width-1, height-1)

    mems = list(parse(lines))
    bad = set(mems[:limit])
    for mem in mems[limit:]:
        bad.add(mem)
        costs = shortest_path(width, height, bad, start, end)
        if end not in costs:
            return ','.join(str(m) for m in mem)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
