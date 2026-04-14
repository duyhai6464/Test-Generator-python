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
    p = [read() for _ in range(n)]
    d = [read() for _ in range(n)]
    for i in range(n):
        max_possible = 0
        for j in range(i + 1, n):
            if p[j] > p[i]:
                max_possible += 1
        if d[i] > max_possible:
            return -1
    L = []
    # Duyệt ngược từ n-1 về 0 (chỉ số 0-indexed)
    for i in range(n - 1, -1, -1):
        if d[i] == 0:
            L.append(i)
        else:
            # Tìm vị trí chèn i để có d[i] phần tử p[j] > p[i] ở bên phải
            count = 0
            insert_idx = -1
            for k in range(len(L) - 1, -1, -1):
                if p[L[k]] > p[i]:
                    count += 1
                    if count == d[i]:
                        insert_idx = k
                        break
            L.insert(insert_idx, i)
    q = [0] * n
    for rank, idx in enumerate(L):
        q[idx] = rank + 1
    # print("debug:", L)
    return " ".join(map(str, q))

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))