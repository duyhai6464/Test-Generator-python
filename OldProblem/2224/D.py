import sys

MOD = 998244353


def merge_count(left, right):
    nl = len(left)
    nr = len(right)
    merged = [0] * (nl + nr)
    i = nl - 1
    j = nr - 1
    k = nl + nr - 1
    count = 0

    while i >= 0 and j >= 0:
        li = left[i]
        rj = right[j]
        if li > rj:
            count += j + 1
            merged[k] = li
            i -= 1
        else:
            merged[k] = rj
            j -= 1
        k -= 1

    while i >= 0:
        merged[k] = left[i]
        i -= 1
        k -= 1

    while j >= 0:
        merged[k] = right[j]
        j -= 1
        k -= 1

    return merged, count


def count_inversions(arr):
    m = len(arr)
    if m <= 1:
        return arr, 0

    mid = m // 2
    left, inv_left = count_inversions(arr[:mid])
    right, inv_right = count_inversions(arr[mid:])
    merged, inv_cross = merge_count(left, right)
    return merged, inv_left + inv_right + inv_cross


def count_product_pairs(a, b_sorted, l, r):
    if r - l == 1:
        ai = a[l]
        return [ai * x for x in b_sorted], 0

    mid = (l + r) // 2
    left, cnt_left = count_product_pairs(a, b_sorted, l, mid)
    right, cnt_right = count_product_pairs(a, b_sorted, mid, r)
    merged, cnt_cross = merge_count(left, right)
    return merged, cnt_left + cnt_right + cnt_cross


def solve_case(a, b):
    n = len(a)
    if n == 1:
        return 0

    b_sorted = sorted(b)
    _, total_pairs = count_product_pairs(a, b_sorted, 0, n)
    _, inv_a = count_inversions(a)

    numerator = (total_pairs - n * inv_a) % MOD
    denominator = n * (n - 1)
    return numerator * pow(denominator, MOD - 2, MOD) % MOD


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    out = []

    for _ in range(t):
        n = data[idx]
        idx += 1
        a = data[idx:idx + n]
        idx += n
        b = data[idx:idx + n]
        idx += n
        out.append(str(solve_case(a, b)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
