from array import array
import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])


n, t = read(), read()
a = [read() for _ in range(n)]
max_value = max(a)
present = [False] * (max_value + 1)
for value in a:
    present[value] = True

# ans[x][y] is the longest arithmetic progression in the set that contains
# both values x and y, with x < y.
ans = [array("h", [0]) * (max_value + 1) for _ in range(max_value + 1)]

for d in range(1, max_value + 1):
    for start in range(1, max_value + 1):
        if not present[start]:
            continue
        prev_value = start - d
        if prev_value >= 1 and present[prev_value]:
            continue

        chain = []
        value = start
        while value <= max_value and present[value]:
            chain.append(value)
            value += d

        length = len(chain)
        if length < 2:
            continue

        for i in range(length - 1):
            x = chain[i]
            row = ans[x]
            for j in range(i + 1, length):
                y = chain[j]
                if row[y] < length:
                    row[y] = length

def run():
    l, r = a[read() - 1], a[read() - 1]
    if l > r: l, r = r, l
    return ans[l][r]

for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))