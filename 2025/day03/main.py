import fileinput


def part1(lines):
    total = 0
    for line in lines:
        nums = [int(n) for n in line]
        hi = max(nums[:-1])
        score = None
        for i, l in enumerate(nums):
            if l == hi:
                r = max(nums[i+1:])
                score = int('{}{}'.format(l, r))
                break
        total += score
    return total


def imax(nums):
    im, m = 0, 0
    for i, n in enumerate(nums):
        if n > m:
            im = i
            m = n
    return im, m


def find(ans, nums, rem):
    if rem == 0:
        return ans
    if len(nums) < rem:
        raise Exception()
    i, n = imax(nums[:-(rem-1)] if rem > 1 else nums)

    new = list(ans)
    new.append(n)
    return find(new, nums[i+1:], rem-1)


def part2(lines):
    total = 0
    for line in lines:
        nums = [int(n) for n in line]
        hi = max(nums[:-11])

        opts = []
        for i, l in enumerate(nums):
            if l == hi:
                try:
                    ans = find([l], nums[i+1:], 11)
                    score = int(''.join(str(n) for n in ans))
                    opts.append(score)
                except Exception as e:
                    continue
        assert len(opts) > 0
        score = max(opts)
        total += score
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
