import fileinput
import re

NUMS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}


def part1(lines):
    total = 0
    for line in lines:
        matches = re.findall('\d', line)
        if not matches:
            continue
        first, last = matches[0], matches[-1]
        total += int(first + last)
    return total


def part2(lines):
    pattern = '|'.join(list(NUMS) + ['\d'])
    pattern = r'(?=({}))'.format(pattern)
    total = 0
    for line in lines:
        matches = list(re.finditer(pattern, line))
        first, last = matches[0].group(1), matches[-1].group(1)
        if first in NUMS:
            first = NUMS[first]
        if last in NUMS:
            last = NUMS[last]
        total += int(first + last)
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line)

    print(part1(lines))
    print(part2(lines))
