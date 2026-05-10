import sys

def ask(k):
    print(f"? {k}", flush=True)
    return list(map(int, input().split()))

def answer(x:list):
    print(f"! {len(x)}", flush=True)
    for u, v in x:
        print(u, v, flush=True)

def count_paths(u: int, G: list[dict[int, bool]], memo: list[int]) -> int:
    if memo[u] != -1:
        return memo[u]
    total = 1
    for v in G[u]:
        total += count_paths(v, G, memo)
    memo[u] = total
    return total

def solve():
    n = int(input())
    G = [dict() for _ in range(n + 1)]
    k = 2
    while k < (1 << n):
        path = ask(k)
        if path[0] <= 0:
            break
        for i in range(1, path[0]):
            G[path[i]][path[i + 1]] = True
        memo = [-1] * (n + 1)
        k += count_paths(path[-1], G, memo)
    E: list[tuple] = []
    for i in range(1, n + 1):
        for j in G[i]:
            E.append((i, j))
    answer(E)
    # print(f"G:{G}\nE:{E}", file=sys.stderr)

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        solve()
