import sys
import matplotlib.pyplot as plt
import random

data = list(map(int, sys.stdin.buffer.read().split()))
t = data[0]
ptr = 1
out = []

for _ in range(t):
    n = data[ptr]
    ptr += 1
    points = []
    for i in range(1, n + 1):
        x = data[ptr]
        y = data[ptr + 1]
        ptr += 2
        points.append((y, x, i))

    points.sort()

    left_stack = [0]
    right_stack = [0]
    ans = []
    print(f"points={points}")
    for i in range(1, n):
        xi = points[i][1]

        while left_stack and xi < points[left_stack[-1]][1]:
            j = left_stack.pop()
            if left_stack:
                ans.append(
                    (
                        points[i][2],
                        points[j][2],
                        points[left_stack[-1]][2],
                    )
                )
        left_stack.append(i)

        while right_stack and xi > points[right_stack[-1]][1]:
            j = right_stack.pop()
            if right_stack:
                ans.append(
                    (
                        points[i][2],
                        points[j][2],
                        points[right_stack[-1]][2],
                    )
                )
        right_stack.append(i)
        print(f"i={i}, left_stack={left_stack}, right_stack={right_stack}, ans={len(ans)}")\
    
    id_to_point = {}
    for y, x, idx in points:
        id_to_point[idx] = (x, y)
    # show the points in a scatter plot name it with index points[i][2] and draw the triangles in ans with different colors
    plt.scatter([p[1] for p in points], [p[0] for p in points])
    for y, x, idx in points:
        plt.text(x, y, str(idx))
    for index, (a, b, c) in enumerate(ans, start=1):
        x1, y1 = id_to_point[a]
        x2, y2 = id_to_point[b]
        x3, y3 = id_to_point[c]

        color = (random.random(), random.random(), random.random())

        plt.plot(
            [x1, x2, x3, x1],
            [y1, y2, y3, y1],
            color=color
        )
        # name the triangle and text note it color with the same color as the triangle
        plt.text((x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3, f"{index}:{a},{b},{c}", 
                 color=color, horizontalalignment='center', verticalalignment='center')
        
    plt.show()
    

    out.append(str(len(ans)))
    out.extend(f"{a} {b} {c}" for a, b, c in ans)

sys.stdout.write("\n".join(out))
