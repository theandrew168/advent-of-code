import copy
import fileinput


def part1(lines):
    reports = []
    for line in lines:
        reports.append([int(n) for n in line.split()])

    def is_safe(report):
        if not report == sorted(report) and not report == sorted(report, reverse=True):
            return False
        for i in range(len(report) - 1):
            diff = abs(report[i] - report[i+1])
            if diff < 1 or diff > 3:
                return False
        return True

    total = 0
    for report in reports:
        if is_safe(report):
            total += 1
    return total


def part2(lines):
    reports = []
    for line in lines:
        reports.append([int(n) for n in line.split()])

    def is_safe(report):
        if not report == sorted(report) and not report == sorted(report, reverse=True):
            return False
        for i in range(len(report) - 1):
            diff = abs(report[i] - report[i+1])
            if diff < 1 or diff > 3:
                return False
        return True

    total = 0
    for report in reports:
        if is_safe(report):
            total += 1
            continue
        for i in range(len(report)):
            r = copy.deepcopy(report)
            r.pop(i)
            if is_safe(r):
                total += 1
                break
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
