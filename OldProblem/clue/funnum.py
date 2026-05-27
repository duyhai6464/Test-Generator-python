import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

from collections import Counter, deque
from heapq import heappop, heappush

n, q = read(), read()
left = deque(read() for _ in range(n))
right = deque()

cnt = Counter()
min_heap = []
max_heap = []
bag_size = 0

dx = 0
order = 1

def add_bag(x: int):
    global bag_size
    cnt[x] += 1
    heappush(min_heap, x)
    heappush(max_heap, -x)
    bag_size += 1

def clean_min():
    while min_heap and cnt[min_heap[0]] == 0:
        heappop(min_heap)

def clean_max():
    while max_heap and cnt[-max_heap[0]] == 0:
        heappop(max_heap)

def pop_min() -> int:
    global bag_size
    clean_min()
    x = heappop(min_heap)
    cnt[x] -= 1
    bag_size -= 1
    return x

def pop_max() -> int:
    global bag_size
    clean_max()
    x = -heappop(max_heap)
    cnt[x] -= 1
    bag_size -= 1
    return x

for _ in range(q):
    qt: int = read()
    if qt < 3:
        x = read()
        dx += x if qt % 2 else -x
    elif qt < 5:
        x = read()
        x -= dx
        if qt % 2:
            left.appendleft(x)
        else:
            right.append(x)
    elif qt < 7:
        while left:
            add_bag(left.popleft())
        while right:
            add_bag(right.popleft())
        order = 1 if qt == 5 else -1
    else:
        if qt & 1:
            if left:
                x = left.popleft()
            elif bag_size:
                x = pop_min() if order == 1 else pop_max()
            else:
                x = right.popleft()
        else:
            if right:
                x = right.pop()
            elif bag_size:
                x = pop_max() if order == 1 else pop_min()
            else:
                x = left.pop()
        print(x + dx)


