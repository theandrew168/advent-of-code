import fileinput


def name(c):
    names = {
        '()': 'paren',
        '[]': 'square',
        '{}': 'curly',
        '<>': 'ineq',
    }
    for k, v in names.items():
        if c in k:
            return v


def check_corrupted(line):
    s = []
    for c in line:
        if c in '([{<':
            s.append(name(c))
        else:
            v = s.pop()
            if v != name(c):
                return c


def check_incomplete(line):
    s = []
    for c in line:
        if c in '([{<':
            s.append(name(c))
        else:
            s.pop()

    if len(s) > 0:
        return s


def part1(lines):
    points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    answer = 0
    for line in lines:
        c = check_corrupted(line)
        if c is not None:
            answer += points[c]

    return answer


def part2(lines):
    points = {
        'paren': 1,
        'square': 2,
        'curly': 3,
        'ineq': 4,
    }

    scores = []
    for line in lines:
        if check_corrupted(line):
            continue

        s = check_incomplete(line)
        if s is None:
            continue

        score = 0
        for c in reversed(s):
            score *= 5
            score += points[c]
        scores.append(score)

    scores = sorted(scores)
    idx = int(len(scores) / 2)
    return scores[idx]


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
