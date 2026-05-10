import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = sys.stdin.read().split()
ptr, out = 0, []
def read(t: type = int):
    global ptr, buffer
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run():
    n = read()
    points = [(read(), read()) for _ in range(n)]
    if n < 2:
        return 0
    transformed_points = []
    for x, y in points:
        transformed_points.append((x, y - x**2))

    transformed_points.sort()

    unique_points = []
    if transformed_points:
        unique_points.append(transformed_points[0])
        for i in range(1, len(transformed_points)):
            if transformed_points[i][0] == unique_points[-1][0]:
                unique_points[-1] = transformed_points[i] # Lấy Y cao nhất
            else:
                unique_points.append(transformed_points[i])
    
    if len(unique_points) < 2:
        return 0

    upper_hull = []
    
    def cross_product(o, a, b):
        """Tính tích vô hướng để kiểm tra hướng rẽ (bẻ lái)"""
        # (ax-ox)*(by-oy) - (ay-oy)*(bx-ox)
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    for p in unique_points:
        # Nếu rẽ trái hoặc đi thẳng (cross_product >= 0) thì loại bỏ điểm cũ
        # Ở đây dùng >= 0 để loại bỏ các điểm thẳng hàng trên cạnh bao lồi
        while len(upper_hull) >= 2 and cross_product(upper_hull[-2], upper_hull[-1], p) >= 0:
            upper_hull.pop()
        upper_hull.append(p)

    return len(upper_hull) - 1

t = 1
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))