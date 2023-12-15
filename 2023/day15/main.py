import fileinput


def hash(s):
    h = 0
    for c in s:
        h = (h + ord(c)) * 17 % 256
    return h


def part1(segs):
    return sum(hash(seg) for seg in segs)


def part2(segs):
    lenses = set()
    boxes = [[] for _ in range(256)]
    for seg in segs:
        label, focal = None, None
        if '=' in seg:
            label, focal = seg.split('=')
            focal = int(focal)
        elif '-' in seg:
            label = seg[:-1]

        lenses.add(label)
        index = hash(label)
        box = boxes[index]

        found = None
        for i, b in enumerate(box):
            if b[0] == label:
                found = i
                break

        # add
        if focal is not None:
            if found is not None:
                box[found] = ((label, focal))
            else:
                box.append((label, focal))

        # sub
        else:
            if found is not None:
                box.pop(found)

    total = 0
    for lense in lenses:
        h = hash(lense)
        box = boxes[h]

        index = None
        focal = None
        for i, b in enumerate(box):
            if b[0] == lense:
                index = i
                focal = b[1]
                break

        if index is None:
            continue

        total += (h+1) * (index+1) * focal

    return total


if __name__ == '__main__':
    segs = []
    for line in fileinput.input():
        segs = line.strip().split(',')

    print(part1(segs))
    print(part2(segs))
