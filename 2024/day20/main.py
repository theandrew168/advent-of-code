from collections import deque
import fileinput


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

    q = deque([[start]])
    while q:
        path = q.popleft()

        curr = path[-1]
        if curr in seen:
            continue

        seen.add(curr)
        for adj in adj4(curr):
            x, y = adj
            c = lines[y][x]
            if c == '#':
                continue

            new_path = path + [adj]
            if adj == end:
                return new_path

            q.append(new_path)


def part1(lines):
    width = len(lines[0])
    height = len(lines)
    start, end = find_start_end(lines)

    path = bfs(lines, start, end)
    return len(path) - 1

    total = 0
    for y in range(height):
        for x in range(width):
            if x == 0 or x == width-1:
                continue
            if y == 0 or y == height-1:
                continue
            c = lines[y][x]
            if c == '#':
                total += 1

    path = bfs(lines, start, end)
    print(path)
    print(len(path))
    return total


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
