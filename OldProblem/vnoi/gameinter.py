import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)

from collections import defaultdict

n = int(input())
dp = defaultdict(list)
options = [1, 2, 3, 4, 5]
for v in options: dp[v].append(v)
for i in range(6, n + 1):
    for v in options:
        if len(dp[i - v]) == 0 or (len(dp[i - v]) == 1 and dp[i - v][0] == v):
            dp[i].append(v)

# debug(dp)

turn = int(len(dp[n]) == 0)
a = ['first' ,'second']
print(a[turn], flush=True)

def run(n, turn):
    last = -1
    while True:
        if turn:
            v = int(input())
            if v <= 0:
                return
            n -= v
            last = v
        else:
            for v in dp[n]:
                if v != last:
                    print(v, flush=True)
                    n -= v
                    last = v
                    break
            else:
                print(-1, flush=True)
                return
        turn = 1 - turn
    # debug(turn, n)

run(n, turn)