from collections import Counter, namedtuple
import fileinput
from functools import partial
import itertools
import math

Point = namedtuple('Point', 'x y z')
Matrix = namedtuple('Matrix', 'r0 r1 r2')


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


def dist_dense(a_points, b_points):
    dists = Counter()
    for a, b in itertools.product(a_points, b_points):
        d = dist(a, b)
        dists[d] += 1

    return dists


def matmul(matrix, point):
    x, y, z = [dot(point, row) for row in matrix]
    return Point(x, y, z)


def orientations(points):
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

    for xform in xforms:
        xform_func = partial(matmul, xform)
        yield tuple(map(xform_func, points))


def part1(scanners):
    based, others = set(scanners[:1]), set(scanners[1:])

    # align each other scanner for the first one
    while others:
        try:
            for base, other in itertools.product(based.copy(), others.copy()):
                for o in orientations(other):
                    dists = dist_dense(base, o)
                    if any(c >= 12 for c in dists.values()):
                        print('found an alignment!', len(based))
                        based.add(o)
                        others.remove(other)
                        raise StopIteration
        except StopIteration:
            pass


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
            scanners.append(tuple(points))
            continue

        x, y, z = line.split(',')
        x, y, z = int(x), int(y), int(z)

        point = Point(x, y, z)
        points.append(point)

    print(part1(scanners.copy()))
    print(part2(scanners.copy()))
