import fileinput


def simulate(fish):
    nextgen = fish.copy()

    # note the zeroes and copy other values down (age - 1)
    new = nextgen[0]
    for i in range(8):
        nextgen[i] = nextgen[i + 1]

    # zeroes back to 6 and create new fish at 8
    nextgen[6] += new
    nextgen[8] = new

    return nextgen


def part1(fish):
    for _ in range(80):
        fish = simulate(fish)
    return sum(fish)


def part2(fish):
    for _ in range(256):
        fish = simulate(fish)
    return sum(fish)


if __name__ == '__main__':
    # represent fish as a bucket for each age (0-8)
    fish = [0] * 9
    for line in fileinput.input():
        for f in line.strip().split(','):
            f = int(f)
            fish[f] += 1
        break

    print(part1(fish))
    print(part2(fish))
