import sys
from collections import defaultdict

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run():
    n, k = read(), read()
    s = read(str)
    pre = [0] * (n + 1)
    counts = defaultdict(int)
    counts[0] = 1
    arr = [1 if cc == '1' else -1 for cc in s]
    for i in range(n):
        pre[i + 1] = pre[i] + arr[i]
        counts[pre[i + 1]] += 1
    
    initial_beauty = 0
    for val in counts:
        freq = counts[val]
        initial_beauty += freq * (freq - 1) // 2
    max_gain = 0
    for i in range(n - 1):
        if arr[i] != arr[i+1]:
            old_pi_plus_1 = pre[i+1]
            new_pi_plus_1 = pre[i] + arr[i+1]
            f_old = counts[old_pi_plus_1]
            f_new = counts[new_pi_plus_1]
            
            current_gain = f_new - (f_old - 1)
            if current_gain > max_gain:
                max_gain = current_gain
    
    # debug(pre, initial_beauty)
    # debug(counts)
    return initial_beauty + max_gain
    
t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))