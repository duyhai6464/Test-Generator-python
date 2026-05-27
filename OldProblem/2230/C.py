import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)
buffer:list[str] = [] if sys.stdin.isatty() else sys.stdin.read().split()
ptr, out = 0, []

def read(t: type = int):
    global buffer, ptr
    while ptr >= len(buffer): buffer.extend(sys.stdin.readline().split())
    ptr += 1
    return t(buffer[ptr - 1])

def run():
    n = read()
    c = [read() for _ in range(n)]
    S = [count for count in c if count >= 2]
    count1 = sum(1 for count in c if count == 1)
    ans = 0
    # Trường hợp 0: Không có lá bài nào có số lượng >= 2
    if len(S) == 0:
        ans = 0
    # Trường hợp 1: Chỉ có duy nhất 1 loại bài có số lượng >= 2
    elif len(S) == 1:
        cx = S[0]
        # Sức chứa tối đa của 1 khối khép kín là cx // 2
        ans = cx + min(count1, cx // 2)
    # Trường hợp 2: Có từ 2 loại bài có số lượng >= 2 trở lên
    else:
        base_sum = sum(S)
        # Mỗi khối đóng góp sức chứa là (cx - 2) // 2
        capacity = sum((cx - 2) // 2 for cx in S)
        ans = base_sum + min(count1, capacity)
    # Điều kiện bắt buộc: Vòng tròn phải có ít nhất 3 lá bài
    if ans < 3:
        ans = 0
    return ans

t = read()
for _ in range(t):
    output = run()
    if output != None: out.append(output)
    
sys.stdout.write("\n".join(map(str, out)))