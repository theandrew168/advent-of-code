from collections import defaultdict
from functools import cache
import time


# Fluent Python - Chaper 7
def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked


# separate func to make the clock decorator work
def fib_recur_inner(n):
    if n == 1 or n == 2:
        return 1
    return fib_recur_inner(n - 1) + fib_recur_inner(n - 2)

@clock
def fib_recur(n):
    return fib_recur_inner(n)


# separate func to make the clock decorator work
def fib_memo_inner(n, memo):
    if memo[n] is not None:
        result = memo[n]
    else:
        result = fib_memo_inner(n - 1, memo) + fib_memo_inner(n - 2, memo)

    memo[n] = result
    return result
    
@clock
def fib_memo(n):
    memo = [None] * (n + 1)
    memo[1] = 1
    memo[2] = 1

    return fib_memo_inner(n, memo)


# separate func to make the clock decorator work
@cache
def fib_cache_inner(n):
    if n == 1 or n == 2:
        return 1
    return fib_cache_inner(n - 1) + fib_cache_inner(n - 2)

@clock
def fib_cache(n):
    return fib_cache_inner(n)


@clock
def fib_bottom_up(n):
    memo = [None] * (n + 1)
    memo[1] = 1
    memo[2] = 1

    for i in range(3, n + 1):
        memo[i] = memo[i - 1] + memo[i - 2]

    return memo[n]


# based on:
# https://github.com/jonathanpaulson/AdventOfCode/blob/master/2021/21.py
def play_recur_inner(p1, p2, s1, s2):
    # base case: found a winner
    if s1 >= 21:
        return (1, 0)
    if s2 >= 21:
        return (0, 1)

    # recursively play the game
    result = (0, 0)
    for d1 in [1, 2, 3]:
        for d2 in [1, 2, 3]:
            for d3 in [1, 2, 3]:
                # roll and calc score
                roll = d1 + d2 + d3
                new_p1 = (p1 + roll) % 10
                new_s1 = s1 + new_p1 + 1

                # swap pos and score to alternate turns
                x1, y1 = play_recur_inner(p2, new_p1, s2, new_s1)

                # apply wins from recursive results (swap back)
                result = (result[0] + y1, result[1] + x1)

    return result


@clock
def play_recur(p1, p2):
    return max(play_recur_inner(p1, p2, 0, 0))


# based on:
# https://github.com/jonathanpaulson/AdventOfCode/blob/master/2021/21.py
def play_memo_inner(p1, p2, s1, s2, memo):
    # base case: found a winner
    if s1 >= 21:
        return (1, 0)
    if s2 >= 21:
        return (0, 1)

    if (p1, p2, s1, s2) in memo:
        return memo[(p1, p2, s1, s2)]

    # recursively play the game
    result = (0, 0)
    for d1 in [1, 2, 3]:
        for d2 in [1, 2, 3]:
            for d3 in [1, 2, 3]:
                # roll and calc score
                roll = d1 + d2 + d3
                new_p1 = (p1 + roll) % 10
                new_s1 = s1 + new_p1 + 1

                # swap pos and score to alternate turns
                x1, y1 = play_memo_inner(p2, new_p1, s2, new_s1, memo)

                # apply wins from recursive results (swap back)
                result = (result[0] + y1, result[1] + x1)

    memo[(p1, p2, s1, s2)] = result
    return result


@clock
def play_memo(p1, p2):
    return max(play_memo_inner(p1, p2, 0, 0, {}))


# based on:
# https://github.com/jonathanpaulson/AdventOfCode/blob/master/2021/21.py
@cache
def play_cache_inner(p1, p2, s1, s2):
    # base case: found a winner
    if s1 >= 21:
        return (1, 0)
    if s2 >= 21:
        return (0, 1)

    # recursively play the game
    result = (0, 0)
    for d1 in [1, 2, 3]:
        for d2 in [1, 2, 3]:
            for d3 in [1, 2, 3]:
                # roll and calc score
                roll = d1 + d2 + d3
                new_p1 = (p1 + roll) % 10
                new_s1 = s1 + new_p1 + 1

                # swap pos and score to alternate turns
                x1, y1 = play_cache_inner(p2, new_p1, s2, new_s1)

                # apply wins from recursive results (swap back)
                result = (result[0] + y1, result[1] + x1)

    return result


@clock
def play_cache(p1, p2):
    return max(play_cache_inner(p1, p2, 0, 0))


# based on:
# https://pastebin.com/rNinEr2S
@clock
def play_bottom_up(op1, op2):
    # 10 positions for player 1
    # 10 positions for player 2
    # 21 scores for player 1
    # 21 scores for player 2
    # 3 rolls of [1, 2, 3]

    # key = (p1, p2, s1, s2)
    memo = defaultdict(int)
    memo[(op1, op2, 0, 0)] = 1

    # linearly fill each game state
    for s1 in range(21):
        for s2 in range(21):
            for p1 in range(10):
                for p2 in range(10):
                    for d1 in [1, 2, 3]:
                        for d2 in [1, 2, 3]:
                            for d3 in [1, 2, 3]:
                                r1 = d1 + d2 + d3
                                pp1 = (p1 + r1) % 10
                                ss1 = min(s1 + pp1 + 1, 21)
                                if ss1 >= 21:
                                    memo[(pp1, p2, ss1, s2)] += memo[(p1, p2, s1, s2)] 
                                else:
                                    for d4 in [1, 2, 3]:
                                        for d5 in [1, 2, 3]:
                                            for d6 in [1, 2, 3]:
                                                r2 = d4 + d5 + d6
                                                pp2 = (p2 + r2) % 10
                                                ss2 = min(s2 + pp2 + 1, 21)
                                                memo[(pp1, pp2, ss1, ss2)] += memo[(p1, p2, s1, s2)] 

    # calc the number of games each player won
    w1, w2 = 0, 0
    for p1 in range(10):
        for p2 in range(10):
            for s in range(21):
                w1 += memo[(p1, p2, 21, s)]
                w2 += memo[(p1, p2, s, 21)]

    return max([w1, w2])


if __name__ == '__main__':
    fib_recur(35)
    fib_memo(35)
    fib_cache(35)
    fib_bottom_up(35)

    # takes way too long
    #play_recur(4, 8)
    play_memo(4, 8)
    play_cache(4, 8)
    play_bottom_up(4, 8)
