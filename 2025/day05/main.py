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


def part2(lines):
    ranges, _= parse(lines)

    rs = []
    for lo, hi in ranges:
        print(lo, hi, rs)
        # detect and merge overlapping ranges
        merged = False
        for i in range(len(rs)):
            rlo, rhi = rs[i]
            # no overlap, skip
            if lo > rhi or hi < rlo:
                continue
            # same range, skip
            if lo == rlo and hi == rhi:
                merged = True
                continue
            # subset, skip
            if lo >= rlo and hi <= rhi:
                merged = True
                continue
            # superset, replace
            if lo <= rlo and hi >= rhi:
                rs[i] = (lo, hi)
                merged = True
            # overlap, replace
            nlo = min(lo, rlo)
            nhi = max(hi, rhi)
            rs[i] = (nlo, nhi)
            merged = True

        # otherwise, add the new range to the list
        if not merged:
            rs.append((lo, hi))

    print(rs)

    total = 0
    for lo, hi in rs:
        total += hi - lo
    return total


# 385836385941925 high
if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
