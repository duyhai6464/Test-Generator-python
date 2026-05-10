import sys

def solve():
    # Đọc n
    line = sys.stdin.readline()
    if not line:
        return
    n = int(line.strip())
    
    # Đọc 2 dòng của bảng
    s1 = sys.stdin.readline().strip()
    s2 = sys.stdin.readline().strip()
    
    # Khởi tạo mảng DP với giá trị vô cùng lớn
    dp = [0] * (n + 1)
    
    # Cơ sở quy hoạch động
    # dp[0] = 0 (không tốn chi phí cho 0 cột)
    
    for i in range(1, n + 1):
        # Lựa chọn 1: Đặt thanh dọc ở cột i (chỉ số i-1 trong chuỗi)
        cost_v = 1 if s1[i-1] != s2[i-1] else 0
        dp[i] = dp[i-1] + cost_v
        
        # Lựa chọn 2: Đặt 2 thanh ngang ở cột i-1 và i
        if i >= 2:
            cost_h1 = 1 if s1[i-2] != s1[i-1] else 0
            cost_h2 = 1 if s2[i-2] != s2[i-1] else 0
            dp[i] = min(dp[i], dp[i-2] + cost_h1 + cost_h2)
            
    print(dp[n])

def main():
    line = sys.stdin.readline()
    if line:
        t = int(line.strip())
        for _ in range(t):
            solve()

if __name__ == "__main__":
    main()