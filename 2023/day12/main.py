import fileinput
import functools


def parse(line):
    record, springs = line.split()
    springs = tuple(int(n) for n in springs.split(','))
    return record, springs


@functools.cache
def solve(record, springs):
#    print(record, springs)

    # no more springs...
    if len(springs) == 0:
        # but still data, lose
        if '#' in record:
            return 0
        # and no data, win
        else:
            return 1

    # no more records but have springs, lose
    if len(record) == 0:
        return 0

    # for dot, strip and recur
    if record[0] == '.':
        return solve(record[1:], springs)

    # for unknown, sum both options
    if record[0] == '?':
        return solve('#' + record[1:], springs) + solve('.' + record[1:], springs)

    want = springs[0]

    # range is too short to satisfy, lose
    if len(record) < want:
        return 0

    # range contains dot, lose
    if '.' in record[:want]:
        return 0

    # if we are at the end, continue (### 3)
    if len(record) == want:
        return solve(record[want:], springs[1:])
    # if range ends with possible dot, consume and continue (#?#. 3, #?#? 3)
    elif record[want] in '.?':
        return solve(record[want+1:], springs[1:])
    # else too many adjacent springs to satisfy, lose (####, 3)
    else:
        return 0


def part1(lines):
    total = 0
    for line in lines:
        record, springs = parse(line)
        arrangements = solve(record, springs)
        total +=  arrangements
#        print(arrangements, line)
    return total


def part2(lines):
    total = 0
    for line in lines:
        record, springs = parse(line)
        record = '?'.join([record]*5)
        springs = springs * 5
        arrangements = solve(record, springs)
        total +=  arrangements
#        print(arrangements, line)
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
