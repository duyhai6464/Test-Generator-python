import sys

arr = [0, 1, 5, 2, 6, 4, 9, 3, 7, 8]
p = [3, 1, 2, 3, 4]

def ask(i: int, j: int) -> int:
    print("?", i, j, flush=True)
    if sys.stdin.isatty(): return 1 if arr[i] > arr[j] else 0
    return int(input())


def answer(i: int) -> None:
    print("!", i, 1, flush=True)

def read():
    if sys.stdin.isatty(): return p.pop()
    return int(input())

class TournamentMin:
    def __init__(self, max_index: int):
        self.root = 0
        self.lost_to = [[] for _ in range(max_index + 1)]

    def match(self, i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i
        if ask(i, j):
            self.lost_to[j].append(i)
            return j
        self.lost_to[i].append(j)
        return i

    def tournament(self, candidates: list[int]) -> int:
        if not candidates:
            return 0

        cur = candidates[:]
        while len(cur) > 1:
            nxt = []
            for k in range(0, len(cur) - 1, 2):
                nxt.append(self.match(cur[k], cur[k + 1]))
            if len(cur) & 1:
                nxt.append(cur[-1])
            cur = nxt

        return cur[0]

    def add_range(self, left: int, count: int) -> None:
        if count <= 0:
            return

        new_min = self.tournament(list(range(left, left + count)))
        self.root = self.match(self.root, new_min)

    def pop_min(self) -> int:
        res = self.root
        candidates = self.lost_to[res]
        self.lost_to[res] = []
        self.root = self.tournament(candidates)
        return res


def main() -> None:
    n = read()
    tree = TournamentMin(2000)
    next_index = 1

    for query_id in range(1, n + 1):
        x = read()
        tree.add_range(next_index, x)
        next_index += x

        ans = tree.root
        if query_id < n:
            tree.pop_min()
        answer(ans)


if __name__ == "__main__":
    main()
