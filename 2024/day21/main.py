import fileinput
import functools


# 789
# 456
# 123
#  0A
NUMS = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '0': (1, 3),
    'A': (2, 3),
}

#  ^A
# <v>
DIRS = {
    '^': (1, 0),
    'A': (2, 0),
    '<': (0, 1),
    'v': (1, 1),
    '>': (2, 1),
}


def path_dx(dx):
    if dx > 0:
        return '>' * abs(dx)
    else:
        return '<' * abs(dx)


def path_dy(dy):
    if dy > 0:
        return 'v' * abs(dy)
    else:
        return '^' * abs(dy)


def path_nums(a, b, d):
    ac = NUMS[a]
    bc = NUMS[b]
    dx = bc[0] - ac[0]
    dy = bc[1] - ac[1]

    # same spot, no need to move
    if dx == 0 and dy == 0:
        return ''

    # moving along Y, path is clear
    if dx == 0:
        return path_dy(dy)

    # moving along X, path is clear
    if dy == 0:
        return path_dx(dx)

    # special cases: 0 and A

    # moving from bottom row to left col, go vertical first
    if a in ['0', 'A'] and b in ['7', '4', '1']:
        return path_dy(dy) + path_dx(dx)

    # moving from left col to bottom row, go horizontal first
    if a in ['7', '4', '1'] and b in ['0', 'A']:
        return path_dx(dx) + path_dy(dy)

    # special cases: left / right proximity
    if d == '<' and dx > 0 and dy > 0:
        return path_dy(dy) + path_dx(dx)
    if d == '>' and dx < 0 and dy > 0:
        return path_dy(dy) + path_dx(dx)

    # need to move across both axes, if possible,
    # prefer to continue in the current direction first
    if d in ['^', 'v']:
        return path_dy(dy) + path_dx(dx)
    if d in ['<', '>']:
        return path_dx(dx) + path_dy(dy)

    # otherwise, arbitrarily choose horiz first
    return path_dx(dx) + path_dy(dy)


def path_dirs(a, b):
    ac = DIRS[a]
    bc = DIRS[b]
    dx = bc[0] - ac[0]
    dy = bc[1] - ac[1]

    # moving along Y, path is clear
    if dx == 0:
        return path_dy(dy)

    # moving along X, path is clear
    if dy == 0:
        return path_dx(dx)

    # special cases: ^ and A

    # moving from top row to bottom row, go vertical first
    if a in ['^', 'A']:
        return path_dy(dy) + path_dx(dx)
    # moving from bottom row to top row, go horizontal first
    if b in ['^', 'A']:
        return path_dx(dx) + path_dy(dy)

    # otherwise, arbitrarily choose horiz first
    return path_dx(dx) + path_dy(dy)


@functools.cache
def solve_nums(code):
    curr = 'A'
    d = None

    path = ''
    for c in code:
        p = path_nums(curr, c, d)
        d = p[-1]
        path += p + 'A'
        curr = c

    return path


@functools.cache
def solve_dirs(code):
    curr = 'A'
    path = ''
    for c in code:
        path += path_dirs(curr, c) + 'A'
        curr = c
    return path


def part1(lines):
    #print(path_nums('7', '9', U))
    #print(path_nums('A', '9', U))
    #print(path_nums('9', 'A', U))
    #print(path_nums('A', 'A', U))
    #print(path_nums('7', '3', R))
    #print(path_dirs('A', '<'))
    #print(path_dirs('<', 'A'))
    #print(path_dirs('v', 'A'))
    total = 0
    for code in lines:
        print(code)
        path = solve_nums(code)
        for _ in range(2):
            path = solve_dirs(path)
        print(len(path), path)
        total += len(path) * int(code[:-1])
    return total


def part2(lines):
    total = 0
    for code in lines:
        path = solve_nums(code)
        for i in range(25):
            path = solve_dirs(path)
            print(i, len(path))
        total += len(path) * int(code[:-1])
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
