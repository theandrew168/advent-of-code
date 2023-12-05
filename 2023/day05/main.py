from collections import defaultdict, namedtuple
import fileinput

from more_itertools import grouper

Range = namedtuple('Range', 'start end')
Map = namedtuple('Map', 'src dst')


def intersect(r0, r1):
    # ranges don't intersect
    if r0.end < r1.start or r0.start > r1.end:
        return None

    return Range(max(r0.start, r1.start), min(r0.end, r1.end))


def lookup(curr, maps):
    for m in maps:
        i = intersect(curr, m.src)
        if i is None:
            continue

        offset = i.start - m.src.start
        length = i.end - i.start
        dst = Range(m.dst.start+offset, m.dst.start+offset+length)
        return dst

    # no intersecting mappings, carry forward
    return curr


def parse_maps(lines):
    maps = defaultdict(list)
    keys = []

    key = ''
    for line in lines:
        if not line:
            continue
        if 'seeds' in line:
            seeds = line.split(':')[1].strip()
            seeds = list(int(n) for n in seeds.split())
            maps['seeds'] = seeds
            continue
        if ':' in line:
            key = line.split(':')[0].split()[0]
            keys.append(key)
            continue

        dst, src, r = [int(n) for n in line.split()]
        src = Range(src, src+r-1)
        dst = Range(dst, dst+r-1)
        m = Map(src, dst)
        maps[key].append(m)

    return maps, keys


def part1(lines):
    maps, keys = parse_maps(lines)

    best = None
    for seed in maps['seeds']:
        curr = Range(seed, seed)
        for key in keys:
            curr = lookup(curr, maps[key])
        if best is None or curr.start < best.start:
            best = curr

    return best.start


def part2(lines):
    maps, keys = parse_maps(lines)
    seeds = grouper(maps['seeds'], 2)
    seeds = [Range(seed[0], seed[0]+seed[1]-1) for seed in seeds]

    best = None
    for seed in seeds:
        curr = seed
        for key in keys:
            curr = lookup(curr, maps[key])
        if best is None or curr.start < best.start:
            best = curr

    return best.start


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
