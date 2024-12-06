import copy
import fileinput


def peek(pos, face):
    if face == 'up':
        return (pos[0], pos[1]-1)
    elif face == 'down':
        return (pos[0], pos[1]+1)
    elif face == 'left':
        return (pos[0]-1, pos[1])
    elif face == 'right':
        return (pos[0]+1, pos[1])


def turn(face):
    if face == 'up':
        return 'right'
    elif face == 'down':
        return 'left'
    elif face == 'left':
        return 'up'
    elif face == 'right':
        return 'down'


def part1(lines):
    pos = None
    for y, line in enumerate(lines):
        if pos:
            break
        for x, c in enumerate(line):
            if c == '^':
                pos = (x, y)
                break

    face = 'up'
    path = set()
    path.add(pos)

    width = len(lines[0])
    height = len(lines)
    while True:
        [nx, ny] = peek(pos, face)
        # out of bounds, break
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            break

        item = lines[ny][nx]
        if item == '#':
            face = turn(face)
        else:
            pos = (nx, ny)
            path.add(pos)

    return len(path)


def part2(lines):
    init_pos = None
    for y, line in enumerate(lines):
        if init_pos:
            break
        for x, c in enumerate(line):
            if c == '^':
                init_pos = (x, y)
                break


    width = len(lines[0])
    height = len(lines)
    total = 0

    # check for a loop by changing each cell
    for y in range(height):
        for x in range(width):
            check = copy.deepcopy(lines)

            # skip starting pos
            if (x, y) == init_pos:
                continue
            # skip existing blockers
            if check[y][x] == '#':
                continue

            # rebuild the modified grid
            check[y] = check[y][:x] + '#' + check[y][x+1:]

            pos = init_pos
            face = 'up'

            # track (pos, face) for loop detection
            path = set()
            path.add((pos, face))

            # follow the path and check for a loop
            while True:
                [nx, ny] = peek(pos, face)
                # out of bounds, break
                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    break

                item = check[ny][nx]
                if item == '#':
                    face = turn(face)
                else:
                    pos = (nx, ny)
                    key = (pos, face)
                    if key in path:
                        total += 1
                        break
                    else:
                        path.add(key)

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
