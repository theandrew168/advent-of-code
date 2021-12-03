import fileinput
import numpy as np


def sig_one(a):
    sig = ''
    for r in a.T:
        ones = list(r).count('1')
        zeroes = list(r).count('0')
        if ones >= zeroes:
            sig += '1'
        else:
            sig += '0'

    return sig


def sig_zero(a):
    sig = ''
    for r in a.T:
        ones = list(r).count('1')
        zeroes = list(r).count('0')
        if ones >= zeroes:
            sig += '0'
        else:
            sig += '1'

    return sig


def part1(a):
    gamma = sig_one(a)
    epsilon = sig_zero(a)

    gamma = int(gamma, base=2)
    epsilon = int(epsilon, base=2)

    return gamma * epsilon


def part2(a):
    o2_rating = np.copy(a)
    for i in range(len(sig_one(o2_rating))):
        if len(o2_rating) == 1:
            break

        sig = sig_one(o2_rating)

        new_rating = []
        for r in o2_rating:
            if r[i] == sig[i]:
                new_rating.append(list(r))

        o2_rating = np.array(new_rating)

    co2_rating = np.copy(a)
    for i in range(len(sig_zero(co2_rating))):
        if len(co2_rating) == 1:
            break

        sig = sig_zero(co2_rating)

        new_rating = []
        for r in co2_rating:
            if r[i] == sig[i]:
                new_rating.append(list(r))

        co2_rating = np.array(new_rating)

    o2_rating = ''.join(o2_rating[0])
    co2_rating = ''.join(co2_rating[0])

    o2_rating = int(o2_rating, base=2)
    co2_rating = int(co2_rating, base=2)

    return o2_rating * co2_rating


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(list(line.strip()))

    a = np.array(lines)

    print(part1(a))
    print(part2(a))
