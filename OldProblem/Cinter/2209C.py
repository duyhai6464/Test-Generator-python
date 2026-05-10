def ask(l, r):
    print(f"? {l} {r}", flush=True)
    return int(input())

def answer(x):
    print(f"! {x}", flush=True)

def solve():
    n = int(input())
    for i in range(2, n + 1):
        x = ask(2 * i - 1, 2 * i)
        if x == 1:
            answer(2 * i)
            return
    x = ask(1, 3)
    if x == 1:
        answer(1)
        return
    x = ask(1, 4)
    if x == 1:
        answer(1)
        return
    answer(2)

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        solve()