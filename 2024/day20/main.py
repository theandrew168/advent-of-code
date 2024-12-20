from collections import defaultdict, deque
import fileinput
import functools


def find_start_end(lines):
    width = len(lines[0])
    height = len(lines)

    start = None
    end = None
    for y in range(height):
        for x in range(width):
            c = lines[y][x]
            if c == 'S':
                start = (x, y)
            if c == 'E':
                end = (x, y)

    return start, end


def adj4(pt):
    for y in [-1, 1]:
        yield (pt[0], pt[1] + y)
    for x in [-1, 1]:
        yield (pt[0] + x, pt[1])


def bfs(lines, start, end):
    seen = set()

    q = deque([(0, start)])
    while q:
        cost, curr = q.popleft()
        if curr in seen:
            continue

        seen.add(curr)
        for adj in adj4(curr):
            x, y = adj
            c = lines[y][x]
            if c == '#':
                continue

            new_cost = cost + 1
            if adj == end:
                return new_cost

            q.append((new_cost, adj))


def apply_skip(lines, x, y):
    out = []
    for i, line in enumerate(lines):
        if i == y:
            skip = list(line)
            skip[x] = '.'
            skip = ''.join(skip)
            out.append(skip)
        else:
            out.append(line)
    return out


def follow(lines, start, end):
    path = [start]

    seen = set()
    seen.add(start)

    curr = start
    while curr != end:
        for adj in adj4(curr):
            if adj in seen:
                continue

            x, y = adj
            c = lines[y][x]
            if c == '#':
                continue

            path.append(adj)
            seen.add(adj)
            curr = adj
            break

    return path


@functools.cache
def dist(a, b):
    return abs(b[0]-a[0]) + abs(b[1]-a[1])


def diamond(center, size):
    for yoff in range(-size, size+1):
        for xoff in range(-size, size+1):
            x, y = center
            pt = (x+xoff, y+yoff)
            d = dist(center, pt)
            # skips of size 0 and 1 don't matter
            if d == 0 or d == 1:
                continue
            # return only points with the grid-dist diamond
            if dist(center, pt) <= size:
                yield pt


def solve(path, skip):
    pathset = set(path)

    diffs = defaultdict(int)
    for i, pt in enumerate(path):
        # the score here is the index in the base path
        here = i
        for dpt in diamond(pt, skip):
            # skip doesn't end on the path, continue
            if dpt not in pathset:
                continue

            # the score there is also the index in the base path
            there = path.index(dpt)

            # skipping behind doesn't help, continue
            if there < here:
                continue

            # this skip saves the time diff between here and there
            diff = there - here - dist(pt, dpt)

            # skip didn't add value, continue
            if diff == 0:
                continue

            # found a valid skip! count it!
            diffs[diff] += 1

    return diffs


def part1(lines):
    width = len(lines[0])
    height = len(lines)
    start, end = find_start_end(lines)
    path = follow(lines, start, end)

    diffs = solve(path, 2)
    return sum(v for k, v in diffs.items() if k >= 100)


def part2(lines):
    width = len(lines[0])
    height = len(lines)
    start, end = find_start_end(lines)
    path = follow(lines, start, end)

    diffs = solve(path, 20)
    return sum(v for k, v in diffs.items() if k >= 100)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
