import sys
import math
import random

def solve():
    # Đọc input nhanh
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    r = int(input_data[1])
    
    points = []
    idx = 2
    for _ in range(n):
        points.append((int(input_data[idx]), int(input_data[idx+1])))
        idx += 2
        
    r2 = r * r
    
    # Tính bước nhảy y cho lưới lục giác (đảm bảo làm tròn lên để không overlap)
    y2 = math.ceil(r * math.sqrt(3))
    
    # Mục tiêu 89% số điểm
    target = math.ceil(0.89 * n)
    
    best_dx, best_dy = 0, 0
    best_coverage = -1
    max_tries = 100000
    for _ in range(max_tries):
        # Chọn ngẫu nhiên một offset trong 1 unit cell của lưới
        dx = random.randint(0, 2 * r - 1)
        dy = random.randint(0, y2 - 1)
        covered = 0
        for px, py in points:
            # Tọa độ điểm so với lưới gốc (đã trừ đi offset)
            x = px - dx
            y = py - dy
            
            # Tính dòng thứ n (n_base) của lưới mà y có khả năng rơi vào
            n_base = y // y2
            
            # Ta chỉ cần check điểm ở 2 dòng gần nhất: n_base và n_base + 1
            # Check dòng n = n_base
            cy = n_base * y2 + dy
            dy_sq = (py - cy)**2
            if dy_sq <= r2: # Lọc nhanh: Nếu khoảng cách trục y đã lớn hơn r thì bỏ qua
                x_rem = x - r * n_base
                m_base = x_rem // (2 * r)
                
                # Check 2 ô gần nhất trên dòng
                cx1 = 2 * r * m_base + r * n_base + dx
                if (px - cx1)**2 + dy_sq <= r2:
                    covered += 1
                    continue
                
                cx2 = cx1 + 2 * r
                if (px - cx2)**2 + dy_sq <= r2:
                    covered += 1
                    continue
                    
            # Check dòng n = n_base + 1
            n_next = n_base + 1
            cy = n_next * y2 + dy
            dy_sq = (py - cy)**2
            if dy_sq <= r2:
                x_rem = x - r * n_next
                m_base = x_rem // (2 * r)
                
                cx1 = 2 * r * m_base + r * n_next + dx
                if (px - cx1)**2 + dy_sq <= r2:
                    covered += 1
                    continue
                    
                cx2 = cx1 + 2 * r
                if (px - cx2)**2 + dy_sq <= r2:
                    covered += 1
                    continue
                    
        # Nếu đạt target 89% thì dừng tìm kiếm
        if covered >= target:
            best_dx, best_dy = dx, dy
            break
            
        # Cập nhật kết quả tốt nhất phòng trường hợp xui xẻo chạy hết max_tries
        if covered > best_coverage:
            best_coverage = covered
            best_dx, best_dy = dx, dy

    # Bước cuối: Thu thập tất cả các tâm đã cover ít nhất 1 điểm với offset tốt nhất
    selected_centers = set()
    
    for px, py in points:
        x = px - best_dx
        y = py - best_dy
        
        n_base = y // y2
        
        found = False
        for n_val in (n_base, n_base + 1):
            if found: break
            cy = n_val * y2 + best_dy
            dy_sq = (py - cy)**2
            if dy_sq <= r2:
                x_rem = x - r * n_val
                m_base = x_rem // (2 * r)
                for m_val in (m_base, m_base + 1):
                    cx = 2 * r * m_val + r * n_val + best_dx
                    if (px - cx)**2 + dy_sq <= r2:
                        selected_centers.add((cx, cy))
                        found = True
                        break

    # In kết quả
    print(len(selected_centers))
    for cx, cy in selected_centers:
        print(f"{cx} {cy}")

if __name__ == '__main__':
    solve()