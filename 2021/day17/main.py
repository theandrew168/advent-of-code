from collections import namedtuple
import fileinput

Point = namedtuple('Point', 'x y')


class Probe:

    def __init__(self, xvel, yvel):
        self.pos = Point(0, 0)
        self.vel = Point(xvel, yvel)

    def __str__(self):
        s = 'pos {} vel {}'
        return s.format(self.pos, self.vel)

    def __iter__(self):
        while True:
            yield self.step()

    def step(self):
        x = self.pos.x + self.vel.x
        y = self.pos.y + self.vel.y

        xvel = self.vel.x
        if xvel > 0:
            xvel -= 1
        elif xvel < 0:
            xvel += 1
        yvel = self.vel.y - 1

        self.pos = Point(x, y)
        self.vel = Point(xvel, yvel)
        return self


class Target:

    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def __str__(self):
        s = 'target x({},{}) y({},{})'
        return s.format(self.xmin, self.xmax, self.ymin, self.ymax)

    def __iter__(self):
        for y in range(self.ymin, self.ymax + 1):
            for x in range(self.xmin, self.xmax + 1):
                yield Point(x, y)

    def __contains__(self, point):
        if point.x < self.xmin or point.x > self.xmax:
            return False
        if point.y < self.ymin or point.y > self.ymax:
            return False
        return True

    def beyond(self, point):
        return point.x > self.xmax or point.y < self.ymin


def test(xvel, yvel, target):
    traj = []

    probe = Probe(xvel, yvel)
    traj.append(probe.pos)
    for step in probe:
        traj.append(step.pos)
        if step.pos in target:
            return traj
        if target.beyond(step.pos):
            return None


def part1(target):
    ymax = None
    for yvel in range(1000):
        for xvel in range(1000):
            traj = test(xvel, yvel, target)
            if traj is None:
                continue
            for x, y in traj:
                if ymax is None or y > ymax:
                    ymax = y

    return ymax


def part2(target):
    count = 0
    for yvel in range(-500, 500):
        for xvel in range(1000):
            traj = test(xvel, yvel, target)
            if traj is None:
                continue
            count += 1

    return count


if __name__ == '__main__':
    target = None
    for line in fileinput.input():
        line = line.strip()

        *_, x, y = line.split()
        x = x[:-1]

        _, x = x.split('=')
        _, y = y.split('=')
        xmin, xmax = x.split('..')
        ymin, ymax = y.split('..')
        xmin, xmax = int(xmin), int(xmax)
        ymin, ymax = int(ymin), int(ymax)

        target = Target(xmin, xmax, ymin, ymax)
        break

    print(part1(target))
    print(part2(target))
