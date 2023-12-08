import fileinput
import itertools
import math


def build_graph(lines):
    g = {}
    for line in lines:
        src, _, l, r = line.split()
        l = l[1:-1]
        r = r[:-1]
        g[src] = (l, r)
    return g


def part1(lines):
    seq = lines[0]
    g = build_graph(lines[2:])

    loc = 'AAA'
    total = 0
    for s in itertools.cycle(seq):
        total += 1
        idx = 0 if s == 'L' else 1
        loc = g[loc][idx]
        if loc == 'ZZZ':
            break

    return total


def part2(lines):
    seq = lines[0]
    g = build_graph(lines[2:])

    locs = [n for n in g if n.endswith('A')]

    # find where each starting node ends
    ends = []
    for loc in locs:
        total = 0
        curr = loc
        for s in itertools.cycle(seq):
            total += 1
            idx = 0 if s == 'L' else 1
            curr = g[curr][idx]
            if curr.endswith('Z'):
                ends.append(total)
                break

    # find the LCM of the ending distances
    print(math.lcm(*ends))


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
