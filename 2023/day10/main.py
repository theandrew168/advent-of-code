import fileinput

# lol
import sys
sys.setrecursionlimit(100000)

LINKS = {
    '|': 'NS',
    '-': 'EW',
    'L': 'NE',
    'J': 'NW',
    '7': 'SW',
    'F': 'SE',
    'S': 'NSEW',
    '.': '',
}


def find_start(lines):
    for y, line in enumerate(lines):
        x = line.find('S')
        if x < 0:
            continue
        return (x, y)


def get(lines, pos):
    width, height = len(lines[0]), len(lines)
    x, y = pos
    if x < 0 or x >= width:
        return None
    if y < 0 or y >= height:
        return None
    return lines[y][x]


def adj(lines, pos):
    n = (pos[0], pos[1]-1)
    s = (pos[0], pos[1]+1)
    e = (pos[0]+1, pos[1])
    w = (pos[0]-1, pos[1])
    return n, s, e, w


def trace(lines, start, curr, prev, path):
    c = get(lines, curr)
    [n, s, e, w] = adj(lines, curr)
    [np, sp, ep, wp] = [get(lines, d) for d in [n,s,e,w]]

    if n != prev and 'N' in LINKS[c] and np and 'S' in LINKS[np]:
        if n == start:
            return path
        path.append(n)
        return trace(lines, start, n, curr, path)

    if s != prev and 'S' in LINKS[c] and sp and 'N' in LINKS[sp]:
        if s == start:
            return path
        path.append(s)
        return trace(lines, start, s, curr, path)

    if e != prev and 'E' in LINKS[c] and ep and 'W' in LINKS[ep]:
        if e == start:
            return path
        path.append(e)
        return trace(lines, start, e, curr, path)

    if w != prev and 'W' in LINKS[c] and wp and 'E' in LINKS[wp]:
        if w == start:
            return path
        path.append(w)
        return trace(lines, start, w, curr, path)

    assert False


def inters(lines, path, pt):
    inside = False

    width = len(lines[0])
    for i in range(width):
        chk = (i, pt[1])
        if chk == pt:
            return inside

        p = get(lines, chk)
        link = LINKS[p]

        if p == '|':
            inside = not inside
            continue

        if inside and ('E' in link or 'W' in link):
            continue

        if inside and ('N' in link or 'S' in link):
            inside = not inside
            continue


def part1(lines):
    start = find_start(lines)
    path = trace(lines, start, start, None, [])
    return len(path) // 2 + 1


def part2(lines):
    start = find_start(lines)
    path = trace(lines, start, start, None, [])
    path = set(path)

    total = 0

    width = len(lines[0])
    height = len(lines)
    for y in range(height):
        for x in range(width):
            pt = (x, y)
            c = get(lines, pt)
            if c != '.':
                continue

            if inters(lines, path, pt):
                print(pt)
                total += 1

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
