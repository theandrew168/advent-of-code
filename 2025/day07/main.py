import fileinput
import functools

# Would sorting the input help?
# Is this a DP problem that can be solved with a memo cache (like fib)?
# Is this a path finding problem (dijkstra's, A*, etc)?
# Is this a system of equations (z3, etc)?
# Is this a complex graph problem (networkx, etc)?


def part1(lines):
    grid = [[c for c in line] for line in lines]
    w = len(grid[0])
    h = len(grid)

    total = 0
    for y in range(1, h):
        for x in range(w):
            prev = grid[y-1][x]
            curr = grid[y][x]
            if curr == '.' and prev in ('S', '|'):
                grid[y][x] = '|'
            elif curr == '^' and prev == '|':
                total += 1
                grid[y][x-1] = '|'
                grid[y][x+1] = '|'
    return total


def part2(lines):
    grid = [[c for c in line] for line in lines]
    w = len(grid[0])
    h = len(grid)

    # top-down memo DP
    DP = {}
    def paths(x, y):
        # check the cache first
        if (x, y) in DP:
            return DP[(x, y)]

        # find and count parents
        cnt = 0
        for yy in range(y-1, -1, -1):
            # base case, initial timeline
            if grid[yy][x] == 'S':
                cnt = 1
                break

            # unreachable parent
            if grid[yy][x] == '^':
                break

            # check for left path
            if x-1 >= 0 and grid[yy][x-1] == '^':
                cnt += paths(x-1, yy)

            # check for right path
            if x+1 < w and grid[yy][x+1] == '^':
                cnt += paths(x+1, yy)

        DP[(x, y)] = cnt
        return cnt

    total = 0

    y = h - 1
    for x in range(w):
        total += paths(x, y)

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
