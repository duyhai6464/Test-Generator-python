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
    n = read()
    a = [read() for _ in range(n)]
    sorted_a = sorted(a, reverse=True)
    # remove duplicates
    sorted_a = list(dict.fromkeys(sorted_a))
    return -1 if len(sorted_a) != n else " ".join(map(str, sorted_a))

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))