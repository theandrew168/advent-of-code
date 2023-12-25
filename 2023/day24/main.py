from collections import namedtuple
import fileinput
import itertools

import z3


Vector = namedtuple('Vector', 'x y z')

class Ray:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def __str__(self):
        s = '{}, {} @ {}, {}'
        return s.format(*self.pos, *self.vel)

    def at(self, t):
        x = self.pos.x + self.vel.x * t
        y = self.pos.y + self.vel.y * t
        z = self.pos.z + self.vel.z * t
        return Vector(x, y, z)

    def intersection(self, other):
        az = self.pos
        ad = self.vel
        bs = other.pos
        bd = other.vel

        dx = bs.x - az.x
        dy = bs.y - az.y
        det = bd.x * ad.y - bd.y * ad.x
        if det == 0:
            return None
        u = (dy * bd.x - dx * bd.y) / det
        v = (dy * ad.x - dx * ad.y) / det
        if u < 0 or v < 0:
            return None
        return u, v


def parse(lines):
    for line in lines:
        pos, vel = line.split('@')
        pos = pos.strip()
        vel = vel.strip()
        pos = tuple(float(n) for n in pos.split(', '))
        vel = tuple(float(n) for n in vel.split(', '))
        yield Vector(*pos), Vector(*vel)


def solve1(rays, start, end):
    total = 0
    for a, b in itertools.combinations(rays, 2):
        inter = a.intersection(b)
        if inter is None:
            continue

        at = a.at(inter[0])
        if at[0] < start or at[0] > end:
            continue
        if at[1] < start or at[1] > end:
            continue

        total += 1

    return total


# 44446443386018, 281342848485672, 166638492241385 @ 197, 16, 200
# 119566840879742, 430566433235378, 268387686114969 @ 18, -130, 74
# 433973471892198, 260061119249300, 263051300077633 @ -16, -170, -118
def solve2():
    x, y, z, dx, dy, dz = z3.Ints('x y z dx dy dz')
    x0, y0, z0, dx0, dy0, dz0, t0 = z3.Ints('x0 y0 z0 dx0 dy0 dz0 t0')
    x1, y1, z1, dx1, dy1, dz1, t1 = z3.Ints('x1 y1 z1 dx1 dy1 dz1 t1')
    x2, y2, z2, dx2, dy2, dz2, t2 = z3.Ints('x2 y2 z2 dx2 dy2 dz2 t2')

    equations = [
        x + dx * t0 == x0 + dx0 * t0,
        y + dy * t0 == y0 + dy0 * t0,
        z + dz * t0 == z0 + dz0 * t0,
        x + dx * t1 == x1 + dx1 * t1,
        y + dy * t1 == y1 + dy1 * t1,
        z + dz * t1 == z1 + dz1 * t1,
        x + dx * t2 == x2 + dx2 * t2,
        y + dy * t2 == y2 + dy2 * t2,
        z + dz * t2 == z2 + dz2 * t2,
    ]

    problem = [
        x0 == 44446443386018,
        y0 == 281342848485672,
        z0 == 166638492241385,
        dx0 == 197,
        dy0 == 16,
        dz0 == 200,
        x1 == 119566840879742,
        y1 == 430566433235378,
        z1 == 268387686114969,
        dx1 == 18,
        dy1 == -130,
        dz1 == 74,
        x2 == 433973471892198,
        y2 == 260061119249300,
        z2 == 263051300077633,
        dx2 == -16,
        dy2 == -170,
        dz2 == -118,
    ]

    s = z3.Solver()
    s.add(equations + problem)
    s.check()

    m = s.model()
    return m[x].as_long() + m[y].as_long() + m[z].as_long()


def part1(lines):
    rays = [Ray(pos, rel) for pos, rel in parse(lines)]
    return solve1(rays, 200_000_000_000_000, 400_000_000_000_000)


def part2(lines):
    return solve2()


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
