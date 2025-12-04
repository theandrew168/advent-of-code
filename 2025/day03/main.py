import fileinput
import functools


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


def solve_dp(dp, line, i, used):
    # base case: we reached the desired length
    if used == 12:
        return 0

    # if at end of the line but NOT solved, invalidate this path
    # with a large, negative number
    if i >= len(line):
        return -10**20

    # check if we've already seen this (index, chars used) value
    key = (i, used)
    if key in dp:
        return dp[key]

    # calc score of picking this character
    picked = 10**(11-used) * int(line[i]) + solve_dp(dp, line, i+1, used+1)
    # calc score of NOT picking this character
    skipped = solve_dp(dp, line, i+1, used)

    # pick the highest of the "picked or skipped" paths
    ans = max(picked, skipped)
    dp[key] = ans
    return ans


@functools.cache
def solve_memo(line, i, used):
    # base case: we reached the desired length
    if used == 12:
        return 0

    # if at end of the line but NOT solved, invalidate this path
    # with a large, negative number
    if i >= len(line):
        return -10**20

    # calc score of picking this character
    picked = 10**(11-used) * int(line[i]) + solve_memo(line, i+1, used+1)
    # calc score of NOT picking this character
    skipped = solve_memo(line, i+1, used)

    # pick the highest of the "picked or skipped" paths
    ans = max(picked, skipped)
    return ans


def part2_dp(lines):
    total = 0
    for line in lines:
        # use dp to track the unique (index, chars used) values
        total += solve_dp({}, line, 0, 0)
    return total


def part2_memo(lines):
    total = 0
    for line in lines:
        # use memo to track the unique (line, index, chars used) values
        total += solve_memo(line, 0, 0)
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
    print(part2_dp(lines))
    print(part2_memo(lines))
