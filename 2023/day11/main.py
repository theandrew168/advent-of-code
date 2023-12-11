import fileinput
import itertools


def parse(lines):
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            c = lines[y][x]
            if c == '#':
                yield [x, y]


def expand(points, by=1):
    width = max(point[0] for point in points)
    height = max(point[1] for point in points)

    x = 0
    while x < width:
        if not any(point[0] == x for point in points):
            for point in points:
                if point[0] > x:
                    point[0] += by
            width += by
            x += by + 1
        else:
            x += 1

    y = 0
    while y < height:
        if not any(point[1] == y for point in points):
            for point in points:
                if point[1] > y:
                    point[1] += by
            height += by
            y += by + 1
        else:
            y += 1


def dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def part1(lines):
    points = list(parse(lines))
    expand(points)
    return sum(dist(a, b) for a, b in itertools.combinations(points, 2))


def part2(lines):
    points = list(parse(lines))
    expand(points, by=999999)
    return sum(dist(a, b) for a, b in itertools.combinations(points, 2))


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
