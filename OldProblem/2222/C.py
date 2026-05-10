import sys

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

def run():
    n = read()
    a = [read() for _ in range(n)]
    sort_a = sorted(a)
    target_median = sort_a[n // 2]
    dp = [-1] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        cnt_less = 0
        cnt_greater = 0
        # Duyệt ngược để kiểm tra các đoạn kết thúc tại i-1
        for j in range(i - 1, -1, -1):
            val = a[j]
            if val < target_median:
                cnt_less += 1
            elif val > target_median:
                cnt_greater += 1
            length = i - j
            # Chỉ xét đoạn có độ dài lẻ
            if length % 2 == 1:
                # Điều kiện để median của đoạn là target_median:
                # Số phần tử nhỏ hơn và số phần tử lớn hơn đều không quá (length-1)//2
                # và giá trị target_median phải tồn tại trong đoạn.
                limit = (length - 1) // 2
                if cnt_less <= limit and cnt_greater <= limit:
                    # Kiểm tra xem target_median có trong đoạn không
                    # (Thực tế nếu thỏa mãn 2 điều kiện trên thì target_median chắc chắn có mặt)
                    if dp[j] != -1:
                        if dp[j] + 1 > dp[i]:
                            dp[i] = dp[j] + 1
    return dp[n]

t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(map(str, out)))