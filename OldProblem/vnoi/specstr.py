import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

MOD = 20032024

def run():
    na = 'aouie'
    s = read(str)
    n = len(s)
    arr = [1 if c in na else 0 for c in s]
    pre = [0] * (n + 1)
    for i in range(n): pre[i + 1] = pre[i] + arr[i]
    ans = 0
    # debug(arr, pre)
    for i in range(n):
        if arr[i]:
            cnt_pa = n - i - (pre[n] - pre[i])
            if cnt_pa > 0:
                ans += pow(2, pre[i + 1] - 1, MOD) * (pow(2, cnt_pa, MOD) - 1)
                ans %= MOD
            # debug('------', i, cnt_pa, ans)
        else:
            cnt_na = i + 1 - pre[i + 1]
            if cnt_na > 0:
                ans += pow(2, i - pre[i + 1], MOD) * (pow(2, pre[n] - pre[i + 1], MOD) - 1)
                ans %= MOD
    #         debug(i, cnt_na, ans)
    # debug('----------------', s, ans)
    return (ans + MOD) % MOD

t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))