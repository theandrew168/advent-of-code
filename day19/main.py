from collections import namedtuple
import fileinput

Point = namedtuple('Point', 'x y z')


def part1(scanners):
    print(len(scanners))
    for points in scanners:
        print(points)


def part2(scanners):
    pass


if __name__ == '__main__':
    scanners = []

    points = None
    for line in fileinput.input():
        line = line.strip()

        # check for start of scanner points
        if 'scanner' in line:
            points = []
            continue

        # check for end of scanner points
        if len(line) == 0:
            scanners.append(points)
            continue

        x, y, z = line.split(',')
        x, y, z = int(x), int(y), int(z)

        point = Point(x, y, z)
        points.append(point)

    print(part1(scanners))
    print(part2(scanners))
