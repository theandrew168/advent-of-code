import fileinput


def parse(line):
    p, v = line.split()
    p, v = p[2:], v[2:]
    px, py = p.split(',')
    px, py = int(px), int(py)
    vx, vy = v.split(',')
    vx, vy = int(vx), int(vy)
    return px, py, vx, vy


def part1(lines):
    t = 100
    width = 101
    height = 103
    #width = 11
    #height = 7

    after = []
    for line in lines:
        px, py, vx, vy = parse(line)
        px = (px + (vx * t)) % width
        py = (py + (vy * t)) % height
        after.append((px, py))

    hw = width // 2
    hh = height // 2
    qs = [0, 0, 0, 0]
    for x, y in after:
        if x < hw and y < hh:
            qs[0] += 1
        elif x > hw and y < hh:
            qs[1] += 1
        elif x < hw and y > hh:
            qs[2] += 1
        elif x > hw and y > hh:
            qs[3] += 1

    total = 1
    for q in qs:
        total *= q
    return total


def display(bots, width, height):
    ps = set((x, y) for x, y, _, _ in bots)
    for y in range(height):
        line = ''
        for x in range(width):
            if (x, y) in ps:
                line += '#'
            else:
                line += '.'
        print(line)


def part2(lines):
    width = 101
    height = 103

    t = 0
    bots = [parse(line) for line in lines]
    ps = set((x, y) for x, y, _, _ in bots)

    done = False
    while not done:
        for px, py, _, _ in bots:
            dense = True
            for yoff in range(-1, 2):
                for xoff in range(-1, 2):
                    if xoff == 0 and yoff == 0:
                        continue
                    cx = (px + xoff) #% width
                    cy = (py + yoff) #% height
                    if (cx, cy) not in ps:
                        dense = False
            if dense:
                done = True
                break

        if done:
            break

        next_bots = []
        next_ps = set()
        for bot in bots:
            px, py, vx, vy = bot
            px = (px + vx) % width
            py = (py + vy) % height
            next_bots.append((px, py, vx, vy))
            next_ps.add((px, py))

        bots = next_bots
        ps = next_ps
        t += 1

    #display(bots, width, height)
    #print('t =', t)

    return t


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
