from collections import defaultdict
import fileinput


def parse(lines):
    for line in lines:
        a,b = line.split('~')
        a = list(int(i) for i in a.split(','))
        b = list(int(i) for i in b.split(','))
        yield [a, b]


def inter(a, b):
    return a[0][0] <= b[1][0] and a[1][0] >= b[0][0] and a[0][1] <= b[1][1] and a[1][1] >= b[0][1] and a[0][2] <= b[1][2] and a[1][2] >= b[0][2]


def shift(brick, x=0, y=0, z=0):
    return (
        (brick[0][0]+x, brick[0][1]+y, brick[0][2]+z),
        (brick[1][0]+x, brick[1][1]+y, brick[1][2]+z),
    )


def settle(bricks):
    bricks = sorted(bricks, key=lambda b: b[0][2])
    settled = set()
    supported_by= defaultdict(list)
    for brick in bricks:
        check = shift(brick, z=-1)
        while check[0][2] > 0:
            count = 0
            for s in settled:
                if inter(check, s):
                    count += 1
                    real = shift(check, z=1)
                    supported_by[real].append(s)
            if count >= 1:
                break
            check = shift(check, z=-1)

        check = shift(check, z=1)
        settled.add(check)

    return settled, supported_by


def part1(lines):
    bricks = list(parse(lines))
    settled, supported_by = settle(bricks)

    total = 0
    for s in settled:
        safe = True
        for k,v in supported_by.items():
            if s in v and len(v) == 1:
                safe = False
        if safe:
            total += 1

    return total


def part2(lines):
    bricks = list(parse(lines))
    settled, supported_by = settle(bricks)

    total = 0
    for s in settled:
        fallen = set()
        fallen.add(s)

        # init chain with bricks supported solely by the removed one
        chain = []
        for k,v in supported_by.items():
            if s in v and len(v) == 1:
                chain.append(k)

        # move up the chain, falling bricks that are no longer supported
        while chain:
            b = chain.pop(0)
            fallen.add(b)
            for k,v in supported_by.items():
                if b in v and set(v) <= fallen:
                    chain.append(k)

        fallen.remove(s)
        total += len(fallen)

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
