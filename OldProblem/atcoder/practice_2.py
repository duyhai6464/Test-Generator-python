
to_char = lambda x: chr(x + ord('A'))

n, q = list(map(int, input().split()))
s = [0]
for i in range(1, n):
    l, r = 0, len(s)
    while l < r:
        m = (r - l) >> 1 + l
        print(f"? {to_char(s[m])} {to_char(i)}")
        res = input().strip()
        if res == ">":
            r = m
        else:
            l = m + 1
    s.insert(l, i)
print("!", "".join(to_char(x) for x in s))