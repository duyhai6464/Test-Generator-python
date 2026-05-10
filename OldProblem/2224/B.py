import sys

debug = lambda *x, **y: print(*x, file=sys.stderr, **y)
buffer:list[str] = sys.stdin.read().split()
ptr = 0
out = []
def read(base: int = 10) -> int:
    global ptr, buffer
    while ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return int(buffer[ptr - 1], base)

def read_t(t: type = str):
    global ptr, buffer
    while ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    if t != str: return t(buffer[ptr - 1])
    return buffer[ptr - 1]

from collections import Counter

def run():
    n = read()
    a = [read() for _ in range(n)]
    max_val = max(a)
    counts = Counter(a)
    result = []
    result.append(max_val)
    counts[max_val] -= 1
    if counts[max_val] == 0:
        del counts[max_val]

    current_mex_candidate = 0
    while current_mex_candidate in counts and counts[current_mex_candidate] > 0:
        result.append(current_mex_candidate)
        counts[current_mex_candidate] -= 1
        if counts[current_mex_candidate] == 0:
            del counts[current_mex_candidate]
        current_mex_candidate += 1

    for val in counts:
        result.extend([val] * counts[val])

    total_sum = 0
    current_prefix_max = 0
    current_prefix_mex = 0
    seen_elements = set()

    for x in result:
        if x > current_prefix_max:
            current_prefix_max = x
        
        seen_elements.add(x)
        while current_prefix_mex in seen_elements:
            current_prefix_mex += 1
            
        total_sum += (current_prefix_max + current_prefix_mex)

    print(total_sum)

t = read()
for _ in range(t):
    output = run()
    if output != None:
        out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))