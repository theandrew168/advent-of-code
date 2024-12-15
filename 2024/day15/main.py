import fileinput


class Grid:
    def __init__(self, lines):
        self._lines = lines
        self._width = len(lines[0])
        self._height = len(lines)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def get(self, x, y):
        return self._lines[y][x]

    def adj4(self, x, y):
        for xoff in [-1, 1]:
            xx = x + xoff
            yield (xx, y)

        for yoff in [-1, 1]:
            yy = y + yoff
            yield (x, yy)


def parse(lines):
    grid = []
    insts = []

    mode = 'grid'
    for line in lines:
        if not line:
            mode = 'insts'
            continue
        if mode == 'grid':
            grid.append(list(line))
        if mode == 'insts':
            insts.extend(list(line))

    return grid, insts


def find_robot(grid):
    width = len(grid[0])
    height = len(grid)

    for y in range(height):
        for x in range(width):
            if grid[y][x] == '@':
                return (x, y)


def find_space(grid, robot, inst):
    width = len(grid[0])
    height = len(grid)

    check = list(robot)


def print_grid(grid):
    width = len(grid[0])
    height = len(grid)
    for y in range(height):
        line = ''
        for x in range(width):
            line += grid[y][x]
        print(line)


def part1(lines):
    grid, insts = parse(lines)
    width = len(grid[0])
    height = len(grid)

    robot = find_robot(grid)
    assert robot is not None

    offs = {
        '^': (0, -1),
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0),
    }

    for inst in insts:
        #print_grid(grid)

        rx, ry = robot
        ox, oy = offs[inst]

        mx, my = rx + ox, ry + oy
        check = grid[my][mx]

        # if moving into a wall, done
        if check == '#':
            continue

        # if moving into a space, move and done
        if check == '.':
            grid[my][mx] = '@'
            grid[ry][rx] = '.'
            robot = (mx, my)
            continue

        # if moving into a box...

        # check if there is a space anywhere in the direction
        space = None
        lx, ly = robot
        to_move = [(lx, ly)]
        while space is None:
            # check bounds
            check = grid[ly][lx]
            if check == '#':
                break

            # check space
            if check == '.':
                space = (lx, ly)
                break

            # keep moving
            lx += ox
            ly += oy
            to_move.append((lx, ly))

        # no spaces in that direction, done
        if not space:
            continue

        # shift everything between the robot and space
        to_move = list(reversed(to_move))
        for i in range(len(to_move) - 1):
            tx, ty = to_move[i]
            fx, fy = to_move[i+1]
            grid[ty][tx] = grid[fy][fx]

        # update robot pos
        grid[ry][rx] = '.'
        robot = tuple(to_move[-2])

    total = 0
    for y in range(height):
        for x in range(width):
            check = grid[y][x]
            if check in ['O', '0']:
                total += x + (y * 100)
    return total


def expand(grid):
    big = []
    for line in grid:
        row = []
        for c in line:
            if c == '#':
                row += ['#', '#']
            if c == 'O':
                row += ['[', ']']
            if c == '@':
                row += ['@', '.']
            if c == '.':
                row += ['.', '.']
        big.append(row)
    return big


def part2(lines):
    grid, insts = parse(lines)
    grid = expand(grid)
    width = len(grid[0])
    height = len(grid)

    robot = find_robot(grid)
    assert robot is not None

    offs = {
        '^': (0, -1),
        'v': (0, 1),
        '<': (-1, 0),
        '>': (1, 0),
    }

    for inst in insts:
        #print_grid(grid)
        #print('inst', inst)

        rx, ry = robot
        ox, oy = offs[inst]

        mx, my = rx + ox, ry + oy
        check = grid[my][mx]

        # if moving into a wall, done
        if check == '#':
            continue

        # if moving into a space, move and done
        if check == '.':
            grid[my][mx] = '@'
            grid[ry][rx] = '.'
            robot = (mx, my)
            continue

        # if moving into a box...

        # check if there is a space anywhere in the direction
        if inst in ['<', '>']:
            space = None
            lx, ly = robot
            to_move = [(lx, ly)]
            while space is None:
                # check bounds
                check = grid[ly][lx]
                if check == '#':
                    break

                # check space
                if check == '.':
                    space = (lx, ly)
                    break

                # keep moving
                lx += ox
                ly += oy
                to_move.append((lx, ly))

            # no spaces in that direction, done
            if not space:
                continue

            # shift everything between the robot and space
            to_move = list(reversed(to_move))
            for i in range(len(to_move) - 1):
                tx, ty = to_move[i]
                fx, fy = to_move[i+1]
                grid[ty][tx] = grid[fy][fx]

            # update robot pos
            grid[ry][rx] = '.'
            robot = tuple(to_move[-2])
        else:
            def try_move(x, y):
                tx, ty = x + ox, y + oy
                c = grid[ty][tx]
                if c == '.':
                    return True
                if c == '[':
                    return try_move(tx, ty) and try_move(tx+1, ty)
                if c == ']':
                    return try_move(tx, ty) and try_move(tx-1, ty)
                return False

            def do_move(x, y):
                tx, ty = x + ox, y + oy
                c = grid[ty][tx]
                if c == '[':
                    do_move(tx, ty)
                    do_move(tx+1, ty)
                elif c == ']':
                    do_move(tx, ty)
                    do_move(tx-1, ty)

                grid[ty][tx] = grid[y][x]
                grid[y][x] = '.'

            if try_move(rx, ry):
                do_move(rx, ry)
                robot = (rx + ox, ry + oy)

    total = 0
    for y in range(height):
        for x in range(width):
            check = grid[y][x]
            if check in ['[']:
                total += x + (y * 100)
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
