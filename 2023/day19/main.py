import fileinput
import math


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
        if step == 'R':
            return total
        if step == 'A':
#            print(R)
            return total + math.prod(v[1]-v[0]+1 for v in R.values())
        if ':' not in step:
            return total + solve2(workflows, step, R['x'], R['m'], R['a'], R['s'])

        cond, goto = step.split(':')
        var, ine, num = cond[0], cond[1], cond[2:]
        num = int(num)

        if ine == '<':
            l, r = (R[var][0], num-1), (num, R[var][1])
            if R[var][0] < num:
                R[var] = l
                if goto == 'A':
#                    print(R)
                    total += math.prod(v[1]-v[0]+1 for v in R.values())
                    R[var] = r
                    continue
                if goto == 'R':
                    R[var] = r
                    continue

                total += solve2(workflows, goto, R['x'], R['m'], R['a'], R['s'])
                R[var] = r
            else:
                R[var] = r
                continue

        if ine == '>':
            l, r = (R[var][0], num), (num+1, R[var][1])
            if R[var][1] > num:
                R[var] = r
                if goto == 'A':
#                    print(R)
                    total += math.prod(v[1]-v[0]+1 for v in R.values())
                    R[var] = l
                    continue
                if goto == 'R':
                    R[var] = l
                    continue

                total += solve2(workflows, goto, R['x'], R['m'], R['a'], R['s'])
                R[var] = l
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
