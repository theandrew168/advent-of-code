from collections import defaultdict
import fileinput
import math


def parse(lines):
    for line in lines:
        id, games = line.split(':')
        id = int(id.split()[1].strip())
        games = games.split(';')

        rounds = []
        for game in games:
            sets = [s.strip() for s in game.strip().split(',')]
            round = [(s.split()[1], int(s.split()[0])) for s in sets]
            rounds.append(round)

        yield id, rounds


def part1(lines):
    limits = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    total = 0
    for id, rounds in parse(lines):
        possible = True
        for round in rounds:
            for color, count in round:
                if count > limits[color]:
                    possible = False

        if possible:
            total += id

    return total


def part2(lines):
    total = 0
    for id, rounds in parse(lines):
        mins = {}

        for round in rounds:
            for color, count in round:
                if color not in mins or count > mins[color]:
                    mins[color] = count

        total += math.prod(mins.values())

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line)

    print(part1(lines))
    print(part2(lines))
