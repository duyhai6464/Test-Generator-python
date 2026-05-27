import sys
from heapq import heappop, heappush


class Edge:
    __slots__ = ("to", "rev", "cap", "cost")

    def __init__(self, to, rev, cap, cost):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost


def add_edge(graph, u, v, cap, cost):
    graph[u].append(Edge(v, len(graph[v]), cap, cost))
    graph[v].append(Edge(u, len(graph[u]) - 1, 0, -cost))


def minimum_bricks(a, n, m):
    cells = n * m
    source = cells
    sink = cells + 1
    vertex_count = cells + 2
    graph = [[] for _ in range(vertex_count)]
    inf_cap = 10**30

    for i in range(n):
        row_base = i * m
        up_base = (i - 1) * m
        for j in range(m):
            u = row_base + j
            value = a[i][j]

            add_edge(graph, source if j == 0 else u - 1, u, 1, 0)

            if i == 0:
                add_edge(graph, u, sink, 1, -value)
            else:
                add_edge(graph, u, up_base + j, 1, a[i - 1][j] - value)

            add_edge(graph, source, u, inf_cap, value)
            add_edge(graph, u, sink, inf_cap, 0)

    inf_dist = 10**60
    potential = [inf_dist] * vertex_count
    potential[source] = 0

    order = [(n - 1 - i + j, i * m + j) for i in range(n) for j in range(m)]
    order.sort()
    for u in [source] + [u for _, u in order] + [sink]:
        base = potential[u]
        if base >= inf_dist:
            continue
        for edge in graph[u]:
            if edge.cap:
                nd = base + edge.cost
                if nd < potential[edge.to]:
                    potential[edge.to] = nd

    for i, value in enumerate(potential):
        if value >= inf_dist:
            potential[i] = 0

    min_cost = 0
    while True:
        dist = [inf_dist] * vertex_count
        parent_v = [-1] * vertex_count
        parent_e = [-1] * vertex_count
        dist[source] = 0
        heap = [(0, source)]

        while heap:
            cur_dist, u = heappop(heap)
            if cur_dist != dist[u]:
                continue
            base = cur_dist + potential[u]
            for edge_id, edge in enumerate(graph[u]):
                if edge.cap:
                    nd = base + edge.cost - potential[edge.to]
                    if nd < dist[edge.to]:
                        dist[edge.to] = nd
                        parent_v[edge.to] = u
                        parent_e[edge.to] = edge_id
                        heappush(heap, (nd, edge.to))

        if dist[sink] >= inf_dist:
            break

        real_cost = dist[sink] + potential[sink] - potential[source]
        if real_cost >= 0:
            break

        for v, value in enumerate(dist):
            if value < inf_dist:
                potential[v] += value

        pushed = inf_cap
        v = sink
        while v != source:
            edge = graph[parent_v[v]][parent_e[v]]
            if edge.cap < pushed:
                pushed = edge.cap
            v = parent_v[v]

        v = sink
        while v != source:
            edge = graph[parent_v[v]][parent_e[v]]
            edge.cap -= pushed
            graph[v][edge.rev].cap += pushed
            v = parent_v[v]

        min_cost += real_cost * pushed

    return -min_cost

import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run():
    n, m = read(), read()
    a = []
    for _ in range(n):
        a.append([read() for _ in range(m)])
    return minimum_bricks(a, n, m)

t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))

