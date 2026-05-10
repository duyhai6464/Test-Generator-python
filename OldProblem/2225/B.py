import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    n = len(s)
    # Tạo 2 chuỗi mục tiêu alternating
    t1 = "".join(['a' if i % 2 == 0 else 'b' for i in range(n)])
    t2 = "".join(['b' if i % 2 == 0 else 'a' for i in range(n)])
    
    def check(target):
        # Tìm vị trí đầu tiên và cuối cùng bị sai lệch
        l = -1
        r = -1
        for i in range(n):
            if s[i] != target[i]:
                if l == -1:
                    l = i
                r = i
        
        # Nếu không có vị trí nào sai, s đã là alternating
        if l == -1:
            return True
        
        # Lấy đoạn con cần biến đổi
        sub = s[l:r+1]
        target_sub = target[l:r+1]
        
        # Thao tác bắt buộc là REVERSE
        rev_sub = sub[::-1]
        
        # TH1: Chỉ Reverse
        if rev_sub == target_sub:
            return True
            
        # TH2: Reverse + Flip bit (a -> b, b -> a)
        flipped_rev_sub = "".join(['b' if c == 'a' else 'a' for c in rev_sub])
        if flipped_rev_sub == target_sub:
            return True
            
        return False

    if check(t1) or check(t2):
        print("YES")
    else:
        print("NO")

def main():
    line = sys.stdin.readline()
    if line:
        t = int(line.strip())
        for _ in range(t):
            solve()

if __name__ == "__main__":
    main()