import sys, bisect

debug = lambda *x, **y: print(*x, file=sys.stderr, **y)

def run():
    x1, y1, x2, y2, k = map(int, input().split())
    dx = x2 - x1
    dy = y2 - y1
    # chuẩn hóa
    sx = 1 if dx >= 0 else -1
    sy = 1 if dy >= 0 else -1
    dx, dy = abs(dx), abs(dy)
    swap = False
    if dx < dy:
        swap = True
        dx, dy = dy, dx
    # debug(f"Original: ({x1}, {y1}) to ({x2}, {y2}), k: {k}")
    # debug(f"dx: {dx}, dy: {dy}, swap: {swap}")
    valid_points = []
    for _ in range(k):
        u, v = map(int, input().split())
        u, v = (u - x1) * sx, (v - y1) * sy
        if swap: u, v = v, u
        # Kiểm tra vật phẩm có nằm trên đường đi ngắn nhất không
        if u >= abs(v) and (dx - u) >= abs(dy - v):
            # Biến đổi thành bài toán LIS 2D: X = u-v, Y = u+v
            valid_points.append((u - v, u + v))
        
    valid_points.sort()
    # Tìm LIS không giảm trên Y2 bằng Binary Search
    tails = []
    for point in valid_points:
        idx = bisect.bisect_right(tails, point[1])
        if idx == len(tails):
            tails.append(point[1])
        else:
            tails[idx] = point[1]
    # debug("valid_points:", valid_points)
    # debug("tails:", tails)
    return len(tails)

print(run())