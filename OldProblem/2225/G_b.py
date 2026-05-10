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

def next_permutation(arr):
    n = len(arr)
    i = n - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    if i == -1:
        # Đây là hoán vị cuối cùng, trả về hoán vị đầu tiên
        return arr[::-1]
    # Bước 2: tìm j
    j = n - 1
    while arr[j] <= arr[i]:
        j -= 1
    # Bước 3: hoán đổi
    arr[i], arr[j] = arr[j], arr[i]
    # Bước 4: đảo ngược đoạn sau i
    arr[i + 1:] = reversed(arr[i + 1:])
    return arr

def run():
    n, m = read(), read()
    k = [read() for i in range(m)]
    per = list(range(n))
    all_count = 1
    for i in range(2, n + 1):
        all_count *= i
    
    def check(a):
        for i in range(1, n):
            for ki in k:
                if abs(a[i - 1] - a[i]) % ki == 0:
                    break# find 1 is ok
            else:
                return False
        return True

    for _ in range(all_count):
        if check(per):
            return ' '.join(map(str, per))
        per = next_permutation(per)
    return -1

t = read()
for _ in range(t):
    output = run()
    if output != None:
        out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))