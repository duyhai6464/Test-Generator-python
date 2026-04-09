class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i, val):
        while i <= self.n:
            self.bit[i] += val
            i += i & -i

    def query(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

n, q = map(int, input().split())
arr = list(map(int, input().split()))

B1 = Fenwick(n)
B2 = Fenwick(n)

def range_add(l, r, x):
    # B1
    B1.update(l, x)
    if r + 1 <= n:
        B1.update(r + 1, -x)
    # B2
    B2.update(l, x * (l - 1))
    if r + 1 <= n:
        B2.update(r + 1, -x * r)

# prefix sum (1 -> i)
def prefix_sum(i):
    return B1.query(i) * i - B2.query(i)

# sum l r
def range_sum(l, r):
    return prefix_sum(r) - prefix_sum(l - 1)

for i in range(n):
    range_add(i + 1, i + 1, arr[i])

for _ in range(q):
    # query is "sum l r" or "add l r x"
    query = input().split()
    query_type = query[0]
    l = int(query[1])
    r = int(query[2])
    if query_type == "sum":
        print(range_sum(l, r))
    elif query_type == "add":
        x = int(query[3])
        range_add(l, r, x)