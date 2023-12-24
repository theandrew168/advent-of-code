from collections import namedtuple
import fileinput
import itertools

# < 19447


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
        return (x, y)

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


def solve2D(rays, start, end):
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


def part1(lines):
    rays = [Ray(pos, rel) for pos, rel in parse(lines)]
    return solve2D(rays, 200_000_000_000_000, 400_000_000_000_000)


def part2(lines):
    pass


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
