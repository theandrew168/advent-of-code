import fileinput
import re


def parse(lines):
    counts = [line for line in lines if line.split() and line.split()[0].isdigit()]
    counts = counts[0].split()

    stacks = [list() for _ in range(len(counts))]
    for line in lines:
        if line[1].isdigit():
            break

        indices = range(1, len(counts) * 4, 4)
        for i, idx in enumerate(indices):
            crate = line[idx]
            if crate == ' ':
                continue
            stacks[i].append(crate)

    for stack in stacks:
        stack.reverse()

    moves = [line.strip() for line in lines if line.startswith('move')]
    return stacks, moves


def part1(lines):
    stacks, moves = parse(lines)
    for move in moves:
        num, src, dst = re.findall(r'\d+', move)
        num, src, dst = int(num), int(src), int(dst)
        src, dst = src - 1, dst - 1
        for _ in range(num):
            stacks[dst].append(stacks[src].pop())

    score = [stack[-1] for stack in stacks]
    score = ''.join(score)
    return score


def part2(lines):
    stacks, moves = parse(lines)
    for move in moves:
        num, src, dst = re.findall(r'\d+', move)
        num, src, dst = int(num), int(src), int(dst)
        src, dst = src - 1, dst - 1
        stacks[dst].extend(stacks[src][-num:])
        del stacks[src][-num:]

    score = [stack[-1] for stack in stacks]
    score = ''.join(score)
    return score


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line)

    print(part1(lines))
    print(part2(lines))
