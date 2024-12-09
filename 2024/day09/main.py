import fileinput


def expand(line):
    id = 0
    disk = []
    files = {}
    gaps = {}
    for i, c in enumerate(line):
        if i%2==0:
            files[len(disk)] = int(c)
            disk.extend([id] * int(c))
            id += 1
        else:
            gaps[len(disk)] = int(c)
            disk.extend(['.'] * int(c))
    return disk, files, gaps


def part1(lines):
    disk, _, _ = expand(lines[0])

    start, end = 0, len(disk) - 1
    while start < end:
        # skip leading files
        if disk[start] != '.':
            start += 1
            continue
        # skip trailing spaces
        if disk[end] == '.':
            end -= 1
            continue

        disk[start] = disk[end]
        disk[end] = '.'
        start += 1
        end -= 1

    ck = 0
    for i, block in enumerate(disk):
        if block == '.':
            break
        ck += i * block
    return ck


def part2(lines):
    disk, files, gaps = expand(lines[0])

    # for each file (right to left)
    for fpos in sorted(files.keys(), reverse=True):
        size = files[fpos]
        # search for a gap that fits (left to right)
        for gpos in sorted(gaps.keys()):
            # only move files to the left
            if gpos >= fpos:
                continue
            avail = gaps[gpos]
            if size <= avail:
                disk[gpos:gpos+size] = disk[fpos:fpos+size]
                disk[fpos:fpos+size] = ['.'] * size
                gaps[gpos+size] = avail-size
                del gaps[gpos]
                break

    ck = 0
    for i, block in enumerate(disk):
        if block == '.':
            continue
        ck += i * block
    return ck


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
