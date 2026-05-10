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

MOD = 998244353

# Hàm đếm số lượng j trong [0, k] sao cho f(j) = 0
# f(j) = 0 khi j = 0 hoặc j % 4 == 3
def count_zeros(k):
    if k < 0: return 0
    return (1 + (k + 1) // 4)

# Hàm đếm số lượng j trong [0, k] sao cho f(j) = 1
# f(j) = 1 khi j % 4 == 1
def count_ones(k):
    if k < 0: return 0
    return (k + 3) // 4

def run():
    n, x = read(), read()
    # Khoảng 1: i thuộc [0, x-1]
    cnt1_0 = count_zeros(x - 1)
    cnt1_1 = count_ones(x - 1)
    # Khoảng 2: r thuộc [x, n]
    cnt2_0 = (count_zeros(n) - count_zeros(x - 1))
    cnt2_1 = (count_ones(n) - count_ones(x - 1))

    # Tổng số cặp (i, r) thỏa mãn
    ans = cnt1_0 * cnt2_0 % MOD + cnt1_1 * cnt2_1 % MOD
    return ans % MOD

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))