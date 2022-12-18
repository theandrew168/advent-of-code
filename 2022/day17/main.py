import fileinput


# 1566984124796 high
# 1566272189352
# 1566272188766 low

# cleaned up solution based on:
# https://old.reddit.com/r/adventofcode/comments/znykq2/2022_day_17_solutions/j0kdnnj/
def solve(line):
    # model rocks with complex numbers
    rocks, i = (
        (0, 1, 2, 3),
        (1, 0+1j, 2+1j, 1+2j),
        (0, 1, 2, 2+1j, 2+2j),
        (0, 0+1j, 0+2j, 0+3j),
        (0, 1, 0+1j, 1+1j),
    ), 0
    # convert jet directions to -1 and 1
    jets,  j = [ord(x) - 61 for x in line], 0

    tower = set()
    cache = dict()
    top = 0

    # check if point is unoccupied
    empty = lambda pos: pos.real in range(7) and pos.imag > 0 and pos not in tower
    # check if a rock move is valid
    check = lambda pos, dir, rock: all(empty(pos + dir + r) for r in rock)

    for step in range(int(1e12)):
        # set start pos of new rock
        pos = complex(2, top + 4)

        # print part 1
        if step == 2022:
            print(int(top))

        # use current rock and jet index as cache key
        key = i, j
        if key in cache:
            # pull step and top from cache
            S, T = cache[key]
            d, m = divmod(1e12 - step, step - S)
            if m == 0:
                # print part 1
                print(int(top + (top - T) * d))
                break
        else:
            cache[key] = step, top

        # determine next rock, cycle index
        rock = rocks[i]
        i = (i + 1) % len(rocks)

        # move the current rock until it settles
        while True:
            # determine next jet, cycle index
            jet = jets[j]
            j = (j + 1) % len(jets)

            # check and move left / right
            if check(pos, jet, rock):
                pos += jet

            # check and move down
            if check(pos, -1j, rock):
                pos += -1j
            # else this piece is done moving
            else:
                break

        # add rock to the tower
        tower |= {pos + r for r in rock}

        # compute new top value (based on rock height)
        top = max(top, pos.imag + [1, 0, 2, 2, 3][i])


if __name__ == '__main__':
    line = None
    for line in fileinput.input():
        line = line.strip()

    solve(line)
