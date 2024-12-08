from collections import defaultdict
import fileinput
import itertools


def parse(lines):
    sats = defaultdict(list)

    width = len(lines[0])
    height = len(lines)
    for y in range(height):
        for x in range(width):
            c = lines[y][x]
            if c == '.':
                continue
            sats[c].append((x, y))

    return sats


def part1(lines):
    width = len(lines[0])
    height = len(lines)

    nodes = set()

    sats = parse(lines)
    for sat, points in sats.items():
        for pair in itertools.permutations(points, 2):
            a, b = pair
            sx, sy = b[0] - a[0], b[1] - a[1]

            checks = [
                (a[0]+sx, a[1]+sy),
                (a[0]-sx, a[1]-sy),
                (b[0]+sx, b[1]+sy),
                (b[0]-sx, b[1]-sy),
            ]
            for check in checks:
                # skip sats in pair
                if check in pair:
                    continue
                # skip OOB sats
                if check[0] < 0 or check[0] >= width:
                    break
                if check[1] < 0 or check[1] >= height:
                    break

                nodes.add(check)

    return len(nodes)


def part2(lines):
    width = len(lines[0])
    height = len(lines)

    nodes = set()

    sats = parse(lines)
    for sat, points in sats.items():
        for pair in itertools.permutations(points, 2):
            a, b = pair
            sx, sy = b[0] - a[0], b[1] - a[1]

            # explore pos slope
            check = a
            while True:
                check = (check[0]+sx, check[1]+sy)
                # skip OOB sats
                if check[0] < 0 or check[0] >= width:
                    break
                if check[1] < 0 or check[1] >= height:
                    break

                nodes.add(check)
                
            # explore neg slope
            check = a
            while True:
                check = (check[0]-sx, check[1]-sy)
                # skip OOB sats
                if check[0] < 0 or check[0] >= width:
                    break
                if check[1] < 0 or check[1] >= height:
                    break

                nodes.add(check)

    return len(nodes)


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
