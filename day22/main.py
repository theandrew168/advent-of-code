from collections import namedtuple
import fileinput

Point = namedtuple('Point', 'x y z')


class Cuboid:

    def __init__(self, x0, x1, y0, y1, z0, z1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1

    @classmethod
    def fromstring(cls, s):
        points = []
        for axis in s.split(','):
            p0, p1 = axis.split('=')[1].split('..')
            points += [int(p0), int(p1)]

        return cls(*points)

    @property
    def small(self):
        mins = [self.x0, self.y0, self.z0]
        maxs = [self.x1, self.y1, self.z1]
        return all(p >= -50 for p in mins) and all(p <= 50 for p in maxs)

    def __str__(self):
        s = 'x={}..{},y={}..{},z={}..{}'
        return s.format(self.x0, self.x1, self.y0, self.y1, self.z0, self.z1)

    def __repr__(self):
        r = 'Cuboid({}, {}, {}, {}, {}, {})'
        return r.format(self.x0, self.x1, self.y0, self.y1, self.z0, self.z1)

    def __len__(self):
        x = abs(self.x1 - self.x0) + 1
        y = abs(self.y1 - self.y0) + 1
        z = abs(self.z1 - self.z0) + 1
        return x * y * z

    def __iter__(self):
        for x in range(self.x0, self.x1 + 1):
            for y in range(self.y0, self.y1 + 1):
                for z in range(self.z0, self.z1 + 1):
                    yield Point(x, y, z)

    def intersects(self, other):
        x = (self.x0 <= other.x1 and self.x1 >= other.x0)
        y = (self.y0 <= other.y1 and self.y1 >= other.y0)
        z = (self.z0 <= other.z1 and self.z1 >= other.z0)
        return (x and y and z)

    def __and__(self, other):
        x0 = max(self.x0, other.x0)
        x1 = min(self.x1, other.x1)
        y0 = max(self.y0, other.y0)
        y1 = min(self.y1, other.y1)
        z0 = max(self.z0, other.z0)
        z1 = min(self.z1, other.z1)
        return Cuboid(x0, x1, y0, y1, z0, z1)

    def erase_and_split(self, other):
        assert self.intersects(other)

        # carve along yz plane
        rem = self
        xa = Cuboid(rem.x0, other.x0 - 1,  rem.y0, rem.y1,  rem.z0, rem.z1)
        xb = Cuboid(other.x0, other.x1,    rem.y0, rem.y1,  rem.z0, rem.z1)
        xc = Cuboid(other.x1 + 1, rem.x1,  rem.y0, rem.y1,  rem.z0, rem.z1)

        # carve along xz plane
        rem = xb
        ya = Cuboid(rem.x0, rem.x1,  rem.y0, other.y0 - 1,  rem.z0, rem.z1)
        yb = Cuboid(rem.x0, rem.x1,  other.y0, other.y1,    rem.z0, rem.z1)
        yc = Cuboid(rem.x0, rem.x1,  other.y1 + 1, rem.y1,  rem.z0, rem.z1)

        # carve along xy plane
        rem = yb
        za = Cuboid(rem.x0, rem.x1,  rem.y0, rem.y1,  rem.z0, other.z0 - 1)
        zb = Cuboid(rem.x0, rem.x1,  rem.y0, rem.y1,  other.z0, other.z1)
        zc = Cuboid(rem.x0, rem.x1,  rem.y0, rem.y1,  other.z1 + 1, rem.z1)

        assert len(zb) == len(other)

        cuboids = [xa, xc, ya, yc, za, zc]
        cuboids = [c for c in cuboids if c.intersects(self)]
        return cuboids


class Reactor:

    def __init__(self):
        # invariant: no cuboids overlap
        self.cuboids = []

    def __len__(self):
        return sum(len(c) for c in self.cuboids)

    def __iter__(self):
        yield from self.cuboids

    def on(self, cuboid):
        cuboids = []
        for c in self.cuboids:
            # no intersection, no split
            if not cuboid.intersects(c):
                cuboids.append(c)

            # intersection, split
            else:
                intersected = True
                i = cuboid & c

                # split existing cuboid, erase intersection, add new
                subs = c.erase_and_split(i)
                cuboids.extend(subs)

        cuboids.append(cuboid)
        self.cuboids = cuboids

    def off(self, cuboid):
        cuboids = []
        for c in self.cuboids:
            # no intersection, no split
            if not cuboid.intersects(c):
                cuboids.append(c)

            # intersection, split
            else:
                i = cuboid & c

                # split existing cuboid, erase intersection, ignore new
                subs = c.erase_and_split(i)
                cuboids.extend(subs)

        self.cuboids = cuboids


def part1(cuboids):
    reactor = set()
    for p, c in cuboids:
        if not c.small:
            continue

        if p == 'on':
            reactor |= set(point for point in c)
        else:
            reactor -= set(point for point in c)

    return len(reactor)


def part2(cuboids):
    reactor = Reactor()
    for p, c in cuboids:
        if p == 'on':
            reactor.on(c)
        else:
            reactor.off(c)

    return len(reactor)


if __name__ == '__main__':
    # geometry tests
    box = Cuboid(0, 2, 0, 2, 0, 2)
    assert len(box) == 27
    assert len(Cuboid(0, 0, 0, 0, 0, 0)) == 1

    # intersections
    assert box.intersects(Cuboid(0, 0, 0, 0, 0, 0))
    assert box.intersects(Cuboid(1, 1, 1, 1, 1, 1))
    assert box.intersects(Cuboid(2, 2, 2, 2, 2, 2))
    assert box.intersects(Cuboid(2, 4, 2, 4, 2, 4))
    assert not box.intersects(Cuboid(3, 6, 3, 6, 3, 6))
    assert not box.intersects(Cuboid(-1, -1, -1, -1, -1, -1))
    assert not box.intersects(Cuboid(3, 3, 3, 3, 3, 3))

    # corners
    assert len(box.erase_and_split(Cuboid(0, 0, 0, 0, 0, 0))) == 3
    assert len(box.erase_and_split(Cuboid(0, 1, 0, 1, 0, 1))) == 3
    assert len(box.erase_and_split(Cuboid(2, 2, 2, 2, 2, 2))) == 3

    # center
    assert len(box.erase_and_split(Cuboid(1, 1, 1, 1, 1, 1))) == 6
    assert len(box.erase_and_split(box)) == 0

    # edges
    assert len(box.erase_and_split(Cuboid(1, 1, 0, 0, 0, 0))) == 4
    assert len(box.erase_and_split(Cuboid(1, 1, 0, 0, 0, 0))) == 4
    assert len(box.erase_and_split(Cuboid(0, 0, 0, 2, 0, 0))) == 2
    assert len(box.erase_and_split(Cuboid(1, 1, 0, 2, 0, 0))) == 3

    # negatives
    box = Cuboid(-1, 1, -1, 1, -1, 1)
    assert len(box) == 27

    # intersections
    assert box.intersects(Cuboid(0, 0, 0, 0, 0, 0))
    assert box.intersects(Cuboid(-1, -1, -1, -1, -1, -1))
    assert box.intersects(Cuboid(1, 1, 1, 1, 1, 1))
    assert box.intersects(Cuboid(1, 3, 1, 3, 1, 3))
    assert not box.intersects(Cuboid(2, 4, 2, 4, 2, 4))
    assert not box.intersects(Cuboid(-2, -2, -2, -2, -2, -2))
    assert not box.intersects(Cuboid(2, 2, 2, 2, 2, 2))

    # corners
    assert len(box.erase_and_split(Cuboid(-1, -1, -1, -1, -1, -1))) == 3
    assert len(box.erase_and_split(Cuboid(-1, 0, -1, 0, -1, 0))) == 3
    assert len(box.erase_and_split(Cuboid(1, 1, 1, 1, 1, 1))) == 3

    # center
    assert len(box.erase_and_split(Cuboid(0, 0, 0, 0, 0, 0))) == 6
    assert len(box.erase_and_split(box)) == 0

    # edges
    assert len(box.erase_and_split(Cuboid(0, 0, -1, -1, -1, -1))) == 4
    assert len(box.erase_and_split(Cuboid(0, 0, -1, -1, -1, -1))) == 4
    assert len(box.erase_and_split(Cuboid(-1, -1, -1, 1, -1, -1))) == 2
    assert len(box.erase_and_split(Cuboid(0, 0, -1, 1, -1, -1))) == 3

    cuboids = []
    for line in fileinput.input():
        line = line.strip()
        power, cuboid = line.split()
        cuboid = Cuboid.fromstring(cuboid)
        cuboids.append((power, cuboid))

    print(part1(cuboids))
    print(part2(cuboids))
