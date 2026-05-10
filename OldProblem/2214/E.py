# Dikjstra's algorithm
import heapq
graph = {}

# n, m = map(int, input().split())
# for _ in range(m):
#     v, u, w = map(int, input().split())
#     if v not in graph:
#         graph[v] = []
#     if u not in graph:
#         graph[u] = []
#     graph[v].append((u, w))
#     graph[u].append((v, w))

# go from 1 to 2...n with dikjstra's algorithm
# dist = [float('inf')] * (n + 1)
# dist[1] = 0
# q = [(0, 1)] # (distance, node)
# trace_prev = [0] * (n + 1) # to trace the path
# while len(q) > 0:
#     current_dist, current_node = heapq.heappop(q)
#     if current_dist > dist[current_node]:
#         continue
#     for neighbor, weight in graph.get(current_node, []):
#         distance = current_dist + weight
#         if distance < dist[neighbor]:
#             trace_prev[neighbor] = current_node
#             dist[neighbor] = distance
#             heapq.heappush(q, (distance, neighbor))
# for i in range(2, n + 1):
#     if dist[i] == float('inf'):
#         print(-1)
#     else:
#         print(dist[i])

# it's April Fools Day "Dijkstra" is spelled incorrectly as "Dikjstra"
# we can use Floyd Warshall with a loop order of i, k, then j to find the answer
n, m = map(int, input().split())
dist = [[float('inf')] * (n + 1) for _ in range(n + 1)]
for _ in range(m):
    v, u, w = map(int, input().split())
    dist[v][u] = dist[u][v] = w
for i in range(1, n + 1):
    dist[i][i] = 0
for i in range(1, n + 1):
    for k in range(1, n + 1):
        for j in range(1, n + 1):
            if dist[i][j] > dist[i][k] + dist[k][j]:
                dist[i][j] = dist[i][k] + dist[k][j]

for i in range(2, n + 1):
    if dist[1][i] == float('inf'):
        print(-1)
    else:
        print(dist[1][i])
                