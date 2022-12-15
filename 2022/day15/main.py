from collections import namedtuple
import fileinput
import re


Point = namedtuple('Point', 'x y')


def mdist(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def adj(p):
    yield Point(p.x + 1, p.y)
    yield Point(p.x - 1, p.y)
    yield Point(p.x, p.y + 1)
    yield Point(p.x, p.y - 1)


class Zone:

    def __init__(self, center, dist):
        self.center = center
        self.dist = dist

    def __contains__(self, p):
        return mdist(self.center, p) <= self.dist

    def __iter__(self):
        for x in range(self.dist):
            y = self.dist - x
            yield Point(self.center.x + x, self.center.y + y)
            yield Point(self.center.x + x, self.center.y - y)
            yield Point(self.center.x - x, self.center.y + y)
            yield Point(self.center.x - x, self.center.y - y)

    def bounds(self):
        top = self.center.x + self.dist
        bottom = self.center.x - self.dist
        left = self.center.y - self.dist
        right = self.center.y + self.dist
        return top, bottom, left, right


def parse(lines):
    for line in lines:
        split = re.split(r'\s+|,|:', line)
        sx, sy, bx, by = split[2], split[4], split[10], split[12]
        sx = int(sx.split('=')[1])
        sy = int(sy.split('=')[1])
        bx = int(bx.split('=')[1])
        by = int(by.split('=')[1])
        yield Point(sx, sy), Point(bx, by)


def part1(lines):
    zones = []

    beacons = set()
    for sensor, beacon in parse(lines):
        beacons.add(beacon)

        zone = Zone(sensor, mdist(sensor, beacon))
        zones.append(zone)

    bounds = [zone.bounds() for zone in zones]
    min_left = min(bound[2] for bound in bounds)
    max_right = max(bound[3] for bound in bounds)

    y = 2000000 if min_left < -10 else 10
    score = 0
    for x in range(min_left, max_right + 1):
        p = Point(x, y)
        if any(p in zone and p not in beacons for zone in zones):
            score += 1

    return score


def part2(lines):
    zones = []

    for sensor, beacon in parse(lines):
        zone = Zone(sensor, mdist(sensor, beacon))
        zones.append(zone)

    bounds = [zone.bounds() for zone in zones]
    min_left = min(bound[2] for bound in bounds)
    limit = 4000000 if min_left < -10 else 20

    for zone in zones:
        for e in zone:
            for p in adj(e):
                if p.x < 0 or p.x > limit:
                    continue
                if p.y < 0 or p.y > limit:
                    continue
                if all(p not in zone for zone in zones):
                    return p.x * 4000000 + p.y


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
