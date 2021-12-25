from collections import defaultdict, namedtuple
import fileinput
from functools import partial
import itertools
import math

Point = namedtuple('Point', 'x y z')
Matrix = namedtuple('Matrix', 'r0 r1 r2')

# http://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
xforms = [
    Matrix(
        Point( 1,  0,  0),
        Point( 0,  1,  0),
        Point( 0,  0,  1),
    ),
    Matrix(
        Point( 1,  0,  0),
        Point( 0,  0, -1),
        Point( 0,  1,  0),
    ),
    Matrix(
        Point( 1,  0,  0),
        Point( 0, -1,  0),
        Point( 0,  0, -1),
    ),
    Matrix(
        Point( 1,  0,  0),
        Point( 0,  0,  1),
        Point( 0, -1,  0),
    ),

    Matrix(
        Point( 0, -1,  0),
        Point( 1,  0,  0),
        Point( 0,  0,  1),
    ),
    Matrix(
        Point( 0,  0,  1),
        Point( 1,  0,  0),
        Point( 0,  1,  0),
    ),
    Matrix(
        Point( 0,  1,  0),
        Point( 1,  0,  0),
        Point( 0,  0, -1),
    ),
    Matrix(
        Point( 0,  0, -1),
        Point( 1,  0,  0),
        Point( 0, -1,  0),
    ),

    Matrix(
        Point(-1,  0,  0),
        Point( 0, -1,  0),
        Point( 0,  0,  1),
    ),
    Matrix(
        Point(-1,  0,  0),
        Point( 0,  0, -1),
        Point( 0, -1,  0),
    ),
    Matrix(
        Point(-1,  0,  0),
        Point( 0,  1,  0),
        Point( 0,  0, -1),
    ),
    Matrix(
        Point(-1,  0,  0),
        Point( 0,  0,  1),
        Point( 0,  1,  0),
    ),

    Matrix(
        Point( 0,  1,  0),
        Point(-1,  0,  0),
        Point( 0,  0,  1),
    ),
    Matrix(
        Point( 0,  0,  1),
        Point(-1,  0,  0),
        Point( 0, -1,  0),
    ),
    Matrix(
        Point( 0, -1,  0),
        Point(-1,  0,  0),
        Point( 0,  0, -1),
    ),
    Matrix(
        Point( 0,  0, -1),
        Point(-1,  0,  0),
        Point( 0,  1,  0),
    ),

    Matrix(
        Point( 0,  0, -1),
        Point( 0,  1,  0),
        Point( 1,  0,  0),
    ),
    Matrix(
        Point( 0,  1,  0),
        Point( 0,  0,  1),
        Point( 1,  0,  0),
    ),
    Matrix(
        Point( 0,  0,  1),
        Point( 0, -1,  0),
        Point( 1,  0,  0),
    ),
    Matrix(
        Point( 0, -1,  0),
        Point( 0,  0, -1),
        Point( 1,  0,  0),
    ),

    Matrix(
        Point( 0,  0, -1),
        Point( 0, -1,  0),
        Point(-1,  0,  0),
    ),
    Matrix(
        Point( 0, -1,  0),
        Point( 0,  0,  1),
        Point(-1,  0,  0),
    ),
    Matrix(
        Point( 0,  0,  1),
        Point( 0,  1,  0),
        Point(-1,  0,  0),
    ),
    Matrix(
        Point( 0,  1,  0),
        Point( 0,  0, -1),
        Point(-1,  0,  0),
    ),
]


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


def dot(a, b):
    return (a.x * b.x) + (a.y * b.y) + (a.z * b.z)


def dist(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    dz = b.z - a.z
    d = dx * dx + dy * dy + dz * dz
    return math.sqrt(d)


def mdist(a, b):
    dx = abs(b.x - a.x)
    dy = abs(b.y - a.y)
    dz = abs(b.z - a.z)
    return dx + dy + dz


def dist_dense(a_points, b_points):
    dists = defaultdict(list)
    for a, b in itertools.product(a_points, b_points):
        d = dist(a, b)
        dists[d].append((a, b))

    return dists


def mdist_dense(a_points, b_points):
    dists = defaultdict(list)
    for a, b in itertools.product(a_points, b_points):
        d = mdist(a, b)
        dists[d].append((a, b))

    return dists


def matmul(matrix, point):
    x, y, z = [dot(point, row) for row in matrix]
    return Point(x, y, z)


def orientations(points):
    for xform in xforms:
        xform_func = partial(matmul, xform)
        yield tuple(map(xform_func, points))


def orient(scanners):
    based, others = scanners[:1], set(scanners[1:])

    # orient each other scanner with the first one
    while others:
        try:
            for base, other in itertools.product(based.copy(), others.copy()):
                for o in orientations(other):
                    dists = dist_dense(base, o)
                    if any(len(pts) >= 12 for pts in dists.values()):
                        print('orient:', len(based))
                        based.append(o)
                        others.remove(other)
                        raise StopIteration
        except StopIteration:
            pass

    return based


def align(scanners):
    based, others = scanners[:1], set(scanners[1:])
    translations = [Point(0, 0, 0)]

    # align each other scanner for the first one
    while others:
        try:
            for base, other in itertools.product(based.copy(), others.copy()):
                dists = dist_dense(base, other)
                for d, pts in dists.items():
                    if len(pts) < 12:
                        continue

                    pt = pts[0]
                    translation = sub(pt[1], pt[0])
                    translate_func = partial(add, translation)
                    translated = list(map(translate_func, other))
                    translations.append(translation)

                    based.append(translated)
                    others.remove(other)
                    raise StopIteration
        except StopIteration:
            pass

    return based, translations


def part1(scanners, translations):
    points = set()
    for scanner in scanners:
        for point in scanner:
            points.add(point)

    return len(points)


def part2(scanners, translations):
    dists = mdist_dense(translations, translations)
    return max(dists)


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
            scanners.append(tuple(points))
            continue

        x, y, z = line.split(',')
        x, y, z = int(x), int(y), int(z)

        point = Point(x, y, z)
        points.append(point)

    scanners = orient(scanners)
    scanners, translations = align(scanners)

    print(part1(scanners, translations))
    print(part2(scanners, translations))
