import sys

data = list(map(int, sys.stdin.read().split()))
ptr = 0
out = []

def read():
    global ptr
    if ptr >= len(data):
        raise Exception("No more input")
    res = data[ptr]
    ptr += 1
    return res


def run():
    t, h, u = read(), read(), read()
    res = min(t, u)
    t -= res
    u -= res
    res *= 4
    if t > 0:# u is 0
        best_th = min(t // 2, h)
        h -= best_th
        t -= best_th * 2
        res += best_th * 7
        if h > 0 and t > 0: # t must be < 2, h > 0 so t=1
            res += 5
            h -= 1
            t -= 1
        if t > 0:# h is 0, t can > 2(no limit here) 
            return res + 2 * t + 1
        # t is 0, h can > 0(no limit here)
        return res + h * 3
    # u > 0, t is 0
    # uh no match so just add 3 for each u,h
    return res + 3 * (u + h)

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))