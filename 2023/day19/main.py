import fileinput
import math

#  90560000000000
# 151683687444000
# 373443687444000
# 151527200000000
#  35896635000000
# 151527200000000

# 167409079868000


def parse(lines):
    i = lines.index('')
    progs, ratings = lines[:i], lines[i+1:]

    workflows = {}
    for prog in progs:
        name, flow = prog.split('{')
        flow = flow[:-1]
        flow = flow.split(',')
        flow = tuple(flow)
        workflows[name] = flow

    ratings = [rating[1:-1] for rating in ratings]
    ratings = [rating.split(',') for rating in ratings]
    ratings = [dict(r.split('=') for r in rating) for rating in ratings]
    ratings = [{k: int(v) for k, v in rating.items()} for rating in ratings]

    return workflows, ratings


def solve1(workflows, rating):
    name = 'in'
    while True:
        workflow = workflows[name]
        for step in workflow:
            if step == 'R':
                return False
            if step == 'A':
                return True
            if ':' not in step:
                name = step
                break

            cond, goto = step.split(':')
            var, ine, num = cond[0], cond[1], cond[2:]
            num = int(num)

            if ine == '<' and rating[var] < num:
                if goto == 'A':
                    return True
                if goto == 'R':
                    return False

                name = goto
                break

            if ine == '>' and rating[var] > num:
                if goto == 'A':
                    return True
                if goto == 'R':
                    return False

                name = goto
                break


def solve2(workflows, name, x, m, a, s):
    R = {'x': x, 'm': m, 'a': a, 's': s}
    total = 0

    workflow = workflows[name]
    for step in workflow:
        print('checking', step, '...')
        print(name, ' '*(4-len(name)), R)
        if step == 'R':
            return 0
        if step == 'A':
            print(step)
            print(name, ' '*(4-len(name)), R)
            return total + math.prod(v[1]-v[0]+1 for v in R.values())
        if ':' not in step:
            return total + solve2(workflows, step, x, m, a, s)

        cond, goto = step.split(':')
        var, ine, num = cond[0], cond[1], cond[2:]
        num = int(num)

        if ine == '<':
            l, r = (R[var][0], num-1), (num, R[var][1])
            if R[var][0] < num:
                R[var] = l
                if goto == 'A':
                    print(step)
                    print(name, ' '*(4-len(name)), R)
                    total += math.prod(v[1]-v[0]+1 for v in R.values())
                    R[var] = r
                    continue
                if goto == 'R':
                    return 0

                total += solve2(workflows, goto, R['x'], R['m'], R['a'], R['s'])
            else:
                R[var] = r
                continue

        if ine == '>':
            l, r = (R[var][0], num), (num+1, R[var][1])
            if R[var][1] > num:
                R[var] = r
                if goto == 'A':
                    print(step)
                    print(name, ' '*(4-len(name)), R)
                    total += math.prod(v[1]-v[0]+1 for v in R.values())
                    R[var] = l
                    continue
                if goto == 'R':
                    return 0

                total += solve2(workflows, goto, R['x'], R['m'], R['a'], R['s'])
            else:
                R[var] = l
                continue

    return total


def part1(lines):
    workflows, ratings = parse(lines)

    total = 0
    for rating in ratings:
        if solve1(workflows, rating):
            total += sum(v for v in rating.values())

    return total


def part2(lines):
    workflows, _ = parse(lines)
    return solve2(workflows, 'in', (1, 4000), (1, 4000), (1, 4000), (1, 4000))


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines.append(line.strip())

    print(part1(lines))
    print(part2(lines))
