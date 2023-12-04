from collections import namedtuple
import fileinput
import functools

Card = namedtuple('Card', 'id winners numbers')


def parse_cards(lines):
    for line in lines:
        head, tail = line.split(':')
        id = head.split()[-1]
        id = int(id)
        winners, numbers = tail.split('|')
        winners = winners.strip().split()
        winners = frozenset(int(n) for n in winners)
        numbers = numbers.strip().split()
        numbers = frozenset(int(n) for n in numbers)
        card = Card(id, winners, numbers)
        yield card


@functools.lru_cache
def count_cards(cards, index):
    card = cards[index]
    score = len(card.winners & card.numbers)
    if score == 0:
        return 1

    return 1 + sum(count_cards(cards, i) for i in range(index+1,index+score+1))


def part1(lines):
    cards = list(parse_cards(lines))

    total = 0
    for card in cards:
        score = len(card.winners & card.numbers)
        if score == 0:
            continue

        score = pow(2, score-1)
        total += score

    return total


def part2(lines):
    cards = tuple(parse_cards(lines))

    total = 0
    for i in range(len(cards)):
        total += count_cards(cards, i)

    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
