from collections import Counter, namedtuple
import fileinput
import math

Point = namedtuple('Point', 'x y z')

# scanner sees within 1000 units x, y, z
# direction and orientation is random (xyz * up -> 6 * 4 = 24)
# how do the points relate independent of view?
# distances between? use that to trim the search space?


def num_conns(n):
    return (n * (n - 1)) / 2


def num_nodes(c):
    for n in range(100):
        cs = num_conns(n)
        if cs == c:
            return n

    return None


def add(a, b):
    dx = b.x + a.x
    dy = b.y + a.y
    dz = b.z + a.z
    return Point(dx, dy, dz)


def sub(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    dz = b.z - a.z
    return Point(dx, dy, dz)


def dist(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    dz = b.z - a.z
    d = dx * dx + dy * dy + dz * dz
    return math.sqrt(d)


def all_dists(points):
    points = points.copy()

    dists = {}
    while points[1:]:
        pa = points[0]
        for pb in points[1:]:
            d = dist(pa, pb)
            dists[(pa, pb)] = d
        points = points[1:]

    return dists


def pair_with_dist(dists, dist):
    for pair, d in dists.items():
        if d == dist:
            return pair


# determine how to make the other points match the base
def align(base, others):
    xforms = [
        lambda p: Point(p.x, p.y, p.z),
    ]

    print(others)
    for xform in xforms:
        maybe = set(map(xform, others))
        print(base, maybe)
        print(base == maybe)


def part1(scanners):
    scanner_dists = []
    for i, points in enumerate(scanners):
        dists = all_dists(points)
        scanner_dists.append(dists)

    total = sum(len(s) for s in scanners)

    idx = 0
    while scanner_dists[1:]:
        this = scanner_dists[0]
        for i, that in enumerate(scanner_dists[1:], start=1):
            sames = set(this.values()) & set(that.values())
            nodes = num_nodes(len(sames))
            total -= nodes
            if len(sames) >= num_conns(12):
                print(idx, 'overlaps', i + idx)

                pairs = []
                this_pts = set()
                for dist in sames:
                    pair = pair_with_dist(this, dist)
                    this_pts.add(pair[0])
                    this_pts.add(pair[1])

                that_pts = set()
                for dist in sames:
                    pair = pair_with_dist(that, dist)
                    that_pts.add(pair[0])
                    that_pts.add(pair[1])

                print(len(this_pts), this_pts)
                print(len(that_pts), that_pts)
                #align(this_pts, that_pts)

        scanner_dists = scanner_dists[1:]
        idx += 1

    print(total)


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
