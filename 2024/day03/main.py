import fileinput
import re


def part1(lines):
    total = 0
    for line in lines:
        for match in re.finditer(r'mul\(\d{1,3},\d{1,3}\)', line):
            op, a, b, _ = re.split(r'[\(\)\,]', match[0])
            a, b = int(a), int(b)
            total += a * b
    return total


def part2(lines):
    total = 0
    enabled = True
    for line in lines:
        for match in re.finditer(r'(mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\))', line):
            if match[0] == 'do()':
                enabled = True
            elif match[0] == 'don\'t()':
                enabled = False
            elif enabled:
                op, a, b, _ = re.split(r'[\(\)\,]', match[0])
                a, b = int(a), int(b)
                total += a * b
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
