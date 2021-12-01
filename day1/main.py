import fileinput
from itertools import tee


def part1(measurements):
    increased = 0
    current = None
    for m in measurements:
        if current is not None and m > current:
            increased += 1
        current = m

    return increased


def part2(measurements):
    # based on:
    # https://docs.python.org/3/library/itertools.html#itertools.pairwise
    a, b, c = tee(measurements, 3)
    next(b, None)
    next(c, None)
    next(c, None)

    increased = 0
    current = None
    for mset in zip(a, b, c):
        s = sum(mset)
        if current is not None and s > current:
            increased += 1
        current = s

    return increased


if __name__ == '__main__':
    measurements = []
    for line in fileinput.input():
        m = int(line)
        measurements.append(m)

    print(part1(measurements))
    print(part2(measurements))
