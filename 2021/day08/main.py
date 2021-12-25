from collections import defaultdict
import fileinput


def part1(entries):
    count = 0
    for _, digits in entries:
        for digit in digits:
            if len(digit) in [2,3,4,7]:
                count += 1

    return count


def solve(signals):
    segs = [None] * 7

    sig_len = defaultdict(list)
    for signal in signals:
        sig_len[len(signal)].append(set(signal))

    seg_freq = defaultdict(int)
    for signal in signals:
        for s in signal:
            seg_freq[s] += 1

    # grab signals known by unique count
    sig1 = sig_len[2][0]
    sig7 = sig_len[3][0]
    sig4 = sig_len[4][0]
    sig8 = sig_len[7][0]

    # seg 0 = sig7 - sig1
    segs[0] = sig7 - sig1

    # seg 1 = freq 6
    segs[1] = [set(s) for s, f in seg_freq.items() if f == 6][0]

    # seg 2 = freq 8 - segs[0]
    tmp = [set(s) for s, f in seg_freq.items() if f == 8]
    segs[2] = [s for s in tmp if not s & segs[0]][0]

    # seg 3 = freq 7 & sig4
    tmp = [set(s) for s, f in seg_freq.items() if f == 7]
    segs[3] = [s for s in tmp if s & sig4][0]

    # seg 4 = freq 4
    segs[4] = [set(s) for s, f in seg_freq.items() if f == 4][0]

    # seg 5 = freq 9
    segs[5] = [set(s) for s, f in seg_freq.items() if f == 9][0]

    # seg 6 = freq 7 - segs[3]
    tmp = [set(s) for s, f in seg_freq.items() if f == 7]
    segs[6] = [s for s in tmp if not s & segs[3]][0]

    return segs


def part2(entries):
    answer = 0
    for signals, digits in entries:
        segs = solve(signals)
        pats = [
            set(segs[0] | segs[1] | segs[2] | segs[4] | segs[5] | segs[6]), 
            set(segs[2] | segs[5]),
            set(segs[0] | segs[2] | segs[3] | segs[4] | segs[6]),
            set(segs[0] | segs[2] | segs[3] | segs[5] | segs[6]),
            set(segs[1] | segs[2] | segs[3] | segs[5]),
            set(segs[0] | segs[1] | segs[3] | segs[5] | segs[6]),
            set(segs[0] | segs[1] | segs[3] | segs[4] | segs[5] | segs[6]),
            set(segs[0] | segs[2] | segs[5]),
            set(segs[0] | segs[1] | segs[2] | segs[3] | segs[4] | segs[5] | segs[6]),
            set(segs[0] | segs[1] | segs[2] | segs[3] | segs[5] | segs[6]),
        ]

        output = ''
        for digit in digits:
            output += str(pats.index(set(digit)))
        answer += int(output)

    return answer


if __name__ == '__main__':
    entries = []
    for line in fileinput.input():
        signals, digits = line.split('|')
        signals = signals.strip().split()
        digits = digits.strip().split()
        entries.append((signals, digits))

    print(part1(entries))
    print(part2(entries))
