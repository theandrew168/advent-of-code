import fileinput
from pprint import pprint


def build_fs(lines):
    root = {'_parent': None, '_size': 0}
    cwd = root
    for line in lines:
        match line.split():
            case ['$', 'cd', '/']:
                cwd = root
            case ['$', 'cd', '..']:
                cwd = cwd['_parent']
            case ['$', 'cd', d]:
                if d not in cwd:
                    cwd[d] = {'_parent': cwd, '_size': 0}
                cwd = cwd[d]
            case ['$', 'ls']:
                pass
            case ['dir', d]:
                pass
            case [size, f]:
                size = int(size)
                cwd[f] = size

                # apply size up the tree
                d = cwd
                while d:
                    d['_size'] += size
                    d = d['_parent']
            case _:
                raise SystemExit(f'invalid line: {line}')

    return root


def part1(lines):
    fs = build_fs(lines)

    def solve(fs):
        score = 0
        if fs['_size'] <= 100000:
            score += fs['_size']

        for k, v in fs.items():
            if type(v) == dict and k != '_parent':
                score += solve(v)

        return score

    return solve(fs)


def part2(lines):
    fs = build_fs(lines)

    total = 70000000
    want = 30000000

    used = fs['_size']
    unused = total - used

    best = None
    def solve(fs):
        nonlocal best

        size = fs['_size']
        if not best:
            best = size

        if unused + size >= want and size < best:
            best = size

        for k, v in fs.items():
            if type(v) == dict and k != '_parent':
                solve(v)

    solve(fs)
    return best


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
