import fileinput

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

    # buttom-up DP
    dp = {}
#    parent = {}

    def parents(n):
        cnt = 0

        x, y = n
        y -= 1
        while y >= 0:
            if grid[y][x] == 'S':
                return 1
            if grid[y][x] == '^':
                break
            l = grid[y][x-1]
            r = grid[y][x+1]
            if l == '^':
                cnt += 1
            if r == '^':
                cnt += 1

        return cnt

#    def trace(n):
#        curr = n
#        while True:
#            p = parent[curr]
#            if p in dp:
#                return dp[p]
#            curr = p

    total = 1
    for y in range(h):
        for x in range(w):
            prev = grid[y-1][x]
            curr = grid[y][x]

            # base case
            if curr == 'S':
                dp[(x, y)] = 1

            if curr == '.' and prev in ('S', '|'):
                parent[(x, y)] = (x, y-1)

                grid[y][x] = '|'
            elif curr == '^' and prev == '|':
                parent[(x, y)] = (x, y-1)
                parent[(x-1, y)] = (x, y)
                parent[(x+1, y)] = (x, y)

                score = trace((x, y)) * 2
                dp[(x, y)] = score
                total += score

                grid[y][x-1] = '|'
                grid[y][x+1] = '|'

    from pprint import pprint
    pprint(dp)
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
