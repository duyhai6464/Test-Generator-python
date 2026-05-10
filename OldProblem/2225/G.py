import sys, math

sys.setrecursionlimit(100000)

debug = lambda *x, **y: print(*x, file=sys.stderr, **y)
buffer:list[str] = sys.stdin.read().split()
ptr = 0
out = []
def read(base: int = 10) -> int:
    global ptr, buffer
    while ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return int(buffer[ptr - 1], base)

def read_t(t: type = str):
    global ptr, buffer
    while ptr >= len(buffer):
        buffer.extend(sys.stdin.readline().split())
    ptr += 1
    if t != str: return t(buffer[ptr - 1])
    return buffer[ptr - 1]

k = [1] * 20
g = [1] * 20

def get_chain(start, rank):
    if rank == 0:
        return [start], []
    # Lấy chuỗi từ mức thấp hơn (rank-1)
    classes, adds = get_chain(start, rank - 1)
    # Số lần cần nhảy bước k[rank] để bao phủ nhóm mới
    cnt = g[rank - 1] // g[rank]
    for _ in range(1, cnt):
        # Bước nhảy từ phần tử cuối hiện tại
        jump = k[rank]
        adds.append(jump)
        # Điểm bắt đầu mới ở nhóm dư mới
        next_start = (classes[-1] + jump) % k[0]
        # Đệ quy lấy tiếp chuỗi ở nhóm mới đó
        sub_classes, sub_adds = get_chain(next_start, rank - 1)
        classes.extend(sub_classes)
        adds.extend(sub_adds)
    return classes, adds

def run():
    n, m = read(), read()
    for i in range(m):
        k[i] = read()
    g[0] = k[0]
    for i in range(1, m):
        g[i] = math.gcd(g[i - 1], k[i])
    if g[m - 1] > 1: return -1
    if k[0] == 1:
        return ' '.join(map(str, range(n)))
    # Bước 1: Xây dựng chuỗi các nhóm dư (residue classes)
    classes, adds = get_chain(0, m - 1)
    
    # Bước 2: Điền các số thực tế vào hoán vị
    ans = []
    new_begin = 0
    # Gom các số theo nhóm dư mod k[0]
    parts = [[] for _ in range(k[0])]
    for i in range(n):
        parts[i % k[0]].append(i)
        
    vis = [False] * n
    
    for i in range(len(classes)):
        c = classes[i]
        current_part_elements = parts[c]
        
        # Tìm new_end: một số thuộc nhóm dư hiện tại khác với new_begin
        # để từ đó có thể nhảy sang nhóm sau
        new_end = -1
        for x in current_part_elements:
            if x != new_begin:
                new_end = x
                break
        
        # Thêm new_begin
        ans.append(new_begin)
        vis[new_begin] = True
        
        # Thêm các số trung gian trong nhóm
        for x in current_part_elements:
            if x != new_begin and x != new_end:
                ans.append(x)
                vis[x] = True
        
        # Thêm new_end
        if new_end != -1:
            ans.append(new_end)
            vis[new_end] = True
            
            # Tính toán điểm bắt đầu cho nhóm tiếp theo
            if i + 1 < len(classes):
                # add[i] là bước nhảy kj giữa 2 nhóm
                step = adds[i]
                # Thử cả hai hướng nhảy +step hoặc -step để tìm số thực tế
                if new_end + step < n and not vis[new_end + step] and (new_end + step) % k[0] == classes[i+1]:
                    new_begin = new_end + step
                else:
                    new_begin = new_end - step
    return ' '.join(map(str, ans))
    

t = read()
for _ in range(t):
    output = run()
    if output != None:
        out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))