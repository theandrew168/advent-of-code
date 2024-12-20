from collections import defaultdict, deque
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


def part1(lines):
    width = len(lines[0])
    height = len(lines)
    start, end = find_start_end(lines)
    baseline = bfs(lines, start, end)

    diffs = defaultdict(int)
    for y in range(1, height-1):
        for x in range(1, width-1):
            c = lines[y][x]
            if c == '.':
                continue
            skip = apply_skip(lines, x, y)
            cost = bfs(skip, start, end)
            diff = baseline - cost
            diffs[diff] += 1

    return sum(v for k, v in diffs.items() if k >= 100)


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
