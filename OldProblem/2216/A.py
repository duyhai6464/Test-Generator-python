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
    n, k = read(), read()
    a = [read() for _ in range(k)]
    b = [read() for _ in range(n)]
    a.append(int(1e18))
    # store index of each element in b in list
    b_indices: dict = {}
    for i, val in enumerate(b):
        if b_indices.get(val) is None:
            b_indices[val] = []
        b_indices[val].append(i)
    for key in b_indices.keys():
        if len(b_indices.get(key, [])) > a[key - 1]:
            return -1
    res = []
    for key in sorted(b_indices.keys(), reverse=True):
        for i in b_indices[key]:
            for _ in range(b[i], k + 1):
                res.append(i + 1)
    return str(len(res)) + "\n" + " ".join(map(str, res))


t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))