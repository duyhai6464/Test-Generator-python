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
    ans = set()
    limit = int(n**(1/3)) + 1

    # Bước 1: Duyệt b nhỏ (b <= n^(1/3)) - Xử lý mọi k, mọi p
    # Số lần lặp: 10,000 (Rất nhanh)
    for b in range(2, limit + 1):
        digits = []
        temp = n
        while temp > 0:
            digits.append(temp % b)
            temp //= b
        digits.reverse()
        
        L = len(digits)
        # Tối ưu p: chỉ duyệt các ước của L
        for p in range(2, L + 1):
            if L % p == 0:
                is_tidy = True
                for i in range(0, L, p):
                    block_digit = digits[i]
                    for j in range(i, i + p):
                        if digits[j] != block_digit:
                            is_tidy = False; break
                    if not is_tidy: break
                if is_tidy:
                    ans.add((b, p))

    # Bước 2: b lớn (b > n^(1/3)) - Lúc này k chỉ có thể bằng 1
    # TH1: p = 2 => n = d * (b + 1) với d < b
    # Tìm tất cả ước của n để tìm (b+1)
    for i in range(1, int(n ** 0.5) + 1):
        if n % i == 0:
            for x in [i, n // i]: # x đóng vai trò là (b+1)
                b = x - 1
                if b >= 2:
                    d = n // x
                    if d < b:
                        ans.add((b, 2))

    # TH2: p = 3 => n = d * (b^2 + b + 1) với d < b
    # Vì b > n^(1/3) nên d < n^(1/3)
    for d in range(1, limit + 1):
        if n % d == 0:
            target = n // d
            # Giải b^2 + b + (1 - target) = 0
            delta = 1 - 4 * (1 - target)
            if delta > 0:
                sq = int(delta ** 0.5)
                if sq * sq == delta:
                    if (sq - 1) % 2 == 0:
                        b = (sq - 1) // 2
                        if b >= 2 and d < b:
                            ans.add((b, 3))
    return len(ans)

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))