import fileinput


def parse(lines):
    ranges = []
    ids = []

    mode = 'ranges'
    for line in lines:
        if not line:
            mode = 'ids'
            continue

        if mode == 'ranges':
            lo, hi = line.split('-')
            ranges.append((int(lo), int(hi)))
        else:
            ids.append(int(line))

    return ranges, ids


def part1(lines):
    ranges, ids = parse(lines)

    total = 0
    for id in ids:
        for lo, hi in ranges:
            if id >= lo and id <= hi:
                total += 1
                break
    return total


def overlaps(rs, n):
    os = []

    lo, hi = n
    for rlo, rhi in rs:
        # no overlap, skip
        if lo > rhi or hi < rlo:
            continue
        # same, add
        if lo == rlo and hi == rhi:
            os.append((rlo, rhi))
            continue
        # subset, add
        if lo >= rlo and hi <= rhi:
            os.append((rlo, rhi))
            continue
        # superset, add
        if lo <= rlo and hi >= rhi:
            os.append((rlo, rhi))
            continue
        # overlap, add
        os.append((rlo, rhi))

    if os:
        os.append(n)

    return os


# [(3, 5), (10, 14), (16, 20)] + (12, 18) = [(3, 5), (10-20)]
# split into overlaps and non-overlaps
# rs = non-overlaps + best(overlaps)
def merge(rs, n):
    os = overlaps(rs, n)
    if os:
        nrs = [r for r in rs if r not in os]
        nlo = min(r[0] for r in os)
        nhi = max(r[1] for r in os)
        nrs.append((nlo, nhi))
        return nrs
    else:
        nrs = [r for r in rs]
        nrs.append(n)
        return nrs


def part2(lines):
    ranges, _= parse(lines)

    rs = [ranges[0]]
    for r in ranges[1:]:
        rs = merge(rs, r)
        print(rs)

    print(rs)

    total = 0
    for lo, hi in rs:
        total += hi - lo + 1
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
