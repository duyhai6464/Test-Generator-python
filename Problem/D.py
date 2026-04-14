n = int(input())
a = list(map(int, input().split()))


def solve():
    total = sum(a)
    if total % n:
        return -1
    m = total // n
    diff = [ai - m for ai in a]
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i] += diff[i] + prefix[i - 1]
    for i in range(n):
        prefix[i] = abs(prefix[i])
    return sum(prefix)
print(solve())