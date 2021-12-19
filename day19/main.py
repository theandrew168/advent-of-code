from collections import Counter, namedtuple
import fileinput
import itertools
import math

Point = namedtuple('Point', 'x y z')

# scanner sees within 1000 units x, y, z
# direction and orientation is random (xyz * up -> 6 * 4 = 24)
# how do the points relate independent of view?
# distances between? use that to trim the search space?


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


def dist_combos(a_points, b_points):
    alen = len(a_points)
    blen = len(b_points)

    dists = Counter()
    lim = max(alen, blen)
    for a, b in itertools.combinations(range(lim), 2):
        if a >= alen:
            continue
        if b >= blen:
            continue

        s = dist(a_points[a], b_points[b])
        dists[s] += 1

    return dists


def orientations(points):
    flips = [
        lambda p: Point( p.x,  p.y,  p.z),
        lambda p: Point( p.x,  p.y, -p.z),
        lambda p: Point( p.x, -p.y,  p.z),
        lambda p: Point( p.x, -p.y, -p.z),
        lambda p: Point(-p.x,  p.y,  p.z),
        lambda p: Point(-p.x,  p.y, -p.z),
        lambda p: Point(-p.x, -p.y,  p.z),
        lambda p: Point(-p.x, -p.y, -p.z),
    ]

    swaps = [
        lambda p: Point(p.x, p.y, p.z),
        lambda p: Point(p.x, p.z, p.y),
        lambda p: Point(p.y, p.x, p.z),
        lambda p: Point(p.y, p.z, p.x),
        lambda p: Point(p.z, p.x, p.y),
        lambda p: Point(p.y, p.z, p.x),
    ]

    for flip in flips:
        for swap in swaps:
            yield list(map(flip, map(swap, points)))


def part1(scanners):
    for a, b in itertools.combinations(range(len(scanners)), 2):
        print(a, 'o', b)
        ascan = scanners[a]
        bscan = scanners[b]
        for o in orientations(bscan):
            dists = dist_combos(ascan, o)
            print(dists.most_common(2))

        break


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

    zeroes = [
        Point(-618,-824,-621),
        Point(-537,-823,-458),
        Point(-447,-329,318),
        Point(404,-588,-901),
        Point(544,-627,-890),
        Point(528,-643,409),
        Point(-661,-816,-575),
        Point(390,-675,-793),
        Point(423,-701,434),
        Point(-345,-311,381),
        Point(459,-707,401),
        Point(-485,-357,347),
    ]

    ones = [
        Point(686,422,578),
        Point(605,423,415),
        Point(515,917,-361),
        Point(-336,658,858),
        Point(-476,619,847),
        Point(-460,603,-452),
        Point(729,430,532),
        Point(-322,571,750),
        Point(-355,545,-477),
        Point(413,935,-424),
        Point(-391,539,-444),
        Point(553,889,-390),
    ]

    for oo in orientations(ones):
        for a, b in zip(zeroes, oo):
            print(dist(a, b))

    print(part1(scanners.copy()))
    print(part2(scanners.copy()))
