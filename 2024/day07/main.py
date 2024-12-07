import fileinput


def parse(line):
    goal, nums = line.split(': ')
    goal = int(goal)
    nums = [int(n) for n in nums.split()]
    return goal, nums


def evaluate(equation):
    total = equation[0]
    for i in range(1, len(equation), 2):
        op = equation[i]
        num = equation[i+1]
        # return partial solutions for optimizing
        if op == '?':
            return total
        elif op == '+':
            total = total + num
        elif op == '*':
            total = total * num
        elif op == '||':
            total = int(str(total) + str(num))
    return total


def dfs(goal, equation, p2=False):
    # base case: all ops are decided
    total = evaluate(equation)
    if '?' not in equation:
        return total == goal

    # if we are already over the goal, ditch this branch
    if total > goal:
        return False

    idx = equation.index('?')
    add = equation[:idx] + ['+'] + equation[idx+1:]
    mul = equation[:idx] + ['*'] + equation[idx+1:]
    cat = equation[:idx] + ['||'] + equation[idx+1:]
    if p2:
        return dfs(goal, add, p2) or dfs(goal, mul, p2) or dfs(goal, cat, p2)
    else:
        return dfs(goal, add) or dfs(goal, mul)


def part1(lines):
    total = 0
    for line in lines:
        goal, nums = parse(line)

        # insert blank ops (?) into the equation
        equation = []
        for num in nums:
            equation.append(num)
            equation.append('?')
        equation = equation[:-1]

        if dfs(goal, equation):
            total += goal
    return total


def part2(lines):
    total = 0
    for line in lines:
        goal, nums = parse(line)

        # insert blank ops (?) into the equation
        equation = []
        for num in nums:
            equation.append(num)
            equation.append('?')
        equation = equation[:-1]

        if dfs(goal, equation, True):
            total += goal
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
