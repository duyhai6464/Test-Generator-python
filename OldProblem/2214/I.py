# import networkx as nx
# import matplotlib.pyplot as plt
import sys
from collections import deque

data = list(map(int, sys.stdin.buffer.read().split()))
ptr = 0
def read():
    global ptr
    ptr += 1
    return data[ptr - 1]

t = read()
for _ in range(t):
    n = read()
    parent = [read() for i in range(n - 1)]
    type_egdes = [read() for i in range(n - 1)]
    # G = nx.Graph()
    # for i in range(2, n + 1):
    #     G.add_edge(parent[i-2], i, type=type_egdes[i-2])
    # # draw G with type 0: gray nothing, 1: red human, 2: blue robot
    # color_map = {0: 'gray', 1: 'red', 2: 'blue'}
    # edge_colors = [color_map[G[u][v]['type']] for u, v in G.edges()]
    # nx.draw(G, with_labels=True, node_color='lightblue', edge_color=edge_colors)
    # plt.show()
    # human > robot so we set human = 1e6(total maxn = 2e5), robot = 1
    graph = {}
    weight_map = {0: 0, 1: int(1e6), 2: 1}
    for i in range(2, n + 1):
        if i not in graph: graph[i] = []
        if parent[i - 2] not in graph: graph[parent[i - 2]] = []
        graph[i].append((parent[i - 2], weight_map[type_egdes[i - 2]]))
        graph[parent[i - 2]].append((i, weight_map[type_egdes[i - 2]]))
    l = []
    d = [float("inf")] * (n + 1)
    que = deque()
    que.append(1)
    d[1] = 0
    while len(que) > 0:
        u = que.popleft()
        if len(graph.get(u, [])) == 1:
            l.append(u)
        for v, w in graph.get(u, []):
            if d[v] > d[u] + w:
                d[v] = d[u] + w
                que.append(v)
    # print(d, l)
    best = 1e18
    ibest = 1
    for i in l:
        if i > 1 and d[i] < best:
            best = d[i]
            ibest = i
    print(ibest)