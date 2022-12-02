import fileinput

PLAYS = {
    'A': 'r',
    'B': 'p',
    'C': 's',
    'X': 'r',
    'Y': 'p',
    'Z': 's',
}

WINS = {
    'r': 's',
    'p': 'r',
    's': 'p',
}

LOSES = {
    'r': 'p',
    'p': 's',
    's': 'r',
}

SCORES = {
    'r': 1,
    'p': 2,
    's': 3,
}


def part1(lines):
    score = 0
    for line in lines:
        a, b = line.split()
        a, b = PLAYS[a], PLAYS[b]
        score += SCORES[b]

        if WINS[a] == b:
            score += 0
        elif WINS[b] == a:
            score += 6
        if a == b:
            score += 3

    return score


def part2(lines):
    score = 0
    for line in lines:
        a, b = line.split()
        a = PLAYS[a]
        if b == 'X':
            b = WINS[a]
        elif b == 'Z':
            b = LOSES[a]
        else:
            b = a
            

        score += SCORES[b]
        if WINS[a] == b:
            score += 0
        elif WINS[b] == a:
            score += 6

        if a == b:
            score += 3

    return score


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
