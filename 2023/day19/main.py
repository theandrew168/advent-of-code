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


# px{a<2006:qkq,m>2090:A,rfg}
# pv{a>1716:R,A}
# lnx{m>1548:A,A}
# rfg{s<537:gd,x>2440:R,A}
# qs{s>3448:A,lnx}
# qkq{x<1416:A,crn}
# crn{x>2662:A,R}
# in{s<1351:px,qqz}
# qqz{s>2770:qs,m<1801:hdj,R}
# gd{a>3333:R,R}
# hdj{m>838:A,pv}

def solve2(workflows, name, x, m, a, s):
    R = {'x': x, 'm': m, 'a': a, 's': s}
    print(name, ' '*(4-len(name)), R)
    total = 0

    workflow = workflows[name]
    for step in workflow:
        if step == 'R':
            return 0
        if step == 'A':
            return total + math.prod(v[1]-v[0]+1 for v in R.values())
        if ':' not in step:
            return total + solve2(workflows, step, x, m, a, s)

        cond, goto = step.split(':')
        var, ine, num = cond[0], cond[1], cond[2:]
        num = int(num)

        if ine == '<' and R[var][0] < num:
            if goto == 'A':
                R[var] = (R[var][0], num-1)
                total += math.prod(v[1]-v[0]+1 for v in R.values())
                continue
            if goto == 'R':
                return 0

            l, r = (R[var][0], num-1), (num, R[var][1])
            R[var] = l
            total += solve2(workflows, goto, R['x'], R['m'], R['a'], R['s'])
            R[var] = r
            total += solve2(workflows, goto, R['x'], R['m'], R['a'], R['s'])
            continue

        if ine == '>' and R[var][1] > num:
            if goto == 'A':
                R[var] = (num+1, R[var][1])
                total += math.prod(v[1]-v[0]+1 for v in R.values())
                continue
            if goto == 'R':
                return 0

            l, r = (R[var][0], num), (num+1, R[var][1])
            R[var] = l
            total += solve2(workflows, goto, R['x'], R['m'], R['a'], R['s'])
            R[var] = r
            total += solve2(workflows, goto, R['x'], R['m'], R['a'], R['s'])
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
