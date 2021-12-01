import fileinput
from more_itertools import sliding_window


def part1(measurements):
    increased = 0
    current = None
    for m in measurements:
        if current is not None and m > current:
            increased += 1
        current = m

    return increased


def part2(measurements):
    increased = 0
    current = None
    for mset in sliding_window(measurements, 3):
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
