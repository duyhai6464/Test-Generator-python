import random
import string

""""""""""""
# Chuyển alphabet sang mã số để tránh gọi ord() nhiều lần
to_int = lambda c: ord(c) # có thể là ord(c) - ord('a') #(+1)
to_char = lambda i: chr(i)
chars = [i for i in range(to_int('a'), to_int('z') + 1)]

ALPHABET = string.ascii_lowercase
BASE = [998244353] * 2
MODS = [10**9 + 7, 10**9 + 9]
LENGTH = 16

""""""""""""

def get_hash_one(s_indices, base: int, mod: int):
    h = 0
    for c in s_indices:
        h = (h * base + c) % mod
    # p_b = 1
    # for c in s_indices:
    #     h = (h + base * c) % mod
    #     p_b = p_b * base % mod
    return h

def get_hash(s_indices, bases: list[int], mods: list[int]):
    return tuple(get_hash_one(s_indices, b, m) for b, m in zip(bases, mods))

def find_collision_fast(bases=BASE, mods=MODS):
    # Thử tìm với độ dài cố định để tiết kiệm tài nguyên
    # Dùng tuple để lưu hash của MODS
    seen = {}
    # Tối ưu: Tính toán bằng danh sách số nguyên thay vì chuỗi
    print("Đang tìm va chạm (Phương pháp tối ưu hóa bộ nhớ)...")
    count = 0
    while True:
        count += 1
        # Tạo mảng số nguyên đại diện cho chuỗi
        s_indices = tuple(random.choices(chars, k=LENGTH))
        # Tính hash nhanh
        h_tuple = get_hash(s_indices, bases, mods)
        if h_tuple in seen:
            s1_indices = seen[h_tuple]
            print(f'find hash {h_tuple} with value {s1_indices}')
            if s1_indices != s_indices:
                res1 = "".join(map(to_char, s1_indices))
                res2 = "".join(map(to_char, s_indices))
                return res1, res2, h_tuple
        seen[h_tuple] = s_indices
        # Nếu dùng 2 MOD 10^9, bạn thực sự cần rất nhiều RAM.
        if count % 1000000 == 0:
            print(f"Đã thử {count//1000000}M mẫu...")
            if count >= 5000000:
                print(f"EXIT length seen {len(seen)}")
                return '', '', None

def f(h_tuple):
    """
    Hàm biến đổi trạng thái (Deterministic Mapping).
    Từ một giá trị hash, sinh ra chuỗi a-z tiếp theo một cách cố định.
    """
    # Sử dụng h_tuple làm seed để đảm bảo: cùng Hash -> cùng chuỗi tiếp theo
    random.seed(hash(h_tuple))
    next_s = tuple(random.choices(chars, k=LENGTH))
    
    next_hash = get_hash(next_s, BASE, MODS)
    return next_hash, next_s

def find_collision_rho():
    print(f"Bắt đầu tìm va chạm với BASE: {BASE} và MODS: {MODS}")
    
    # Khởi tạo điểm xuất phát
    start_s = tuple(random.choices(chars, k=LENGTH))
    x_hash = get_hash(start_s, BASE, MODS)
    y_hash = x_hash
    
    print("Giai đoạn 1: Tìm điểm gặp nhau trong chu trình...")
    count = 0
    while True:
        x_hash, _ = f(x_hash)           # Rùa nhảy 1 bước
        y_hash, _ = f(f(y_hash)[0])     # Thỏ nhảy 2 bước
        
        count += 1
        if count % 100000 == 0:
            print(f"Đã thực hiện {count/100000}M bước nhảy...")
            
        if x_hash == y_hash:
            print(f"Đã tìm thấy chu trình sau {count} bước.")
            break
            
    print("Giai đoạn 2: Truy tìm điểm va chạm (điểm bắt đầu chu trình)...")
    # Đưa Rùa về vạch xuất phát, Thỏ đứng yên tại điểm gặp nhau
    x_hash = get_hash(start_s, BASE, MODS)
    
    while True:
        next_x_hash, x_str = f(x_hash)
        next_y_hash, y_str = f(y_hash)
        
        # Nếu Hash tiếp theo giống nhau nhưng chuỗi hiện tại khác nhau -> Va chạm!
        if next_x_hash == next_y_hash:
            if x_str != y_str:
                return x_str, y_str, next_x_hash
            else:
                # Trường hợp hiếm: chu trình quá ngắn hoặc x_str == y_str
                print("Lỗi: Chuỗi trùng nhau, đang thử lại với hạt giống khác...")
                return None
        
        x_hash = next_x_hash
        y_hash = next_y_hash

def cmp_hash(s1, s2, bases=BASE, mods=MODS):
    s1_indices = [ord(c) - ord('a') + 1 for c in s1]
    s2_indices = [ord(c) - ord('a') + 1 for c in s2]
    for b, m in zip(bases, mods):
        if get_hash_one(s1_indices, b, m) != get_hash_one(s2_indices, b, m):
            return False
    return True



if __name__ == "__main__":
    # print(cmp_hash("aatamjqxaaaaaaaaaaaakyaeaaaaqgulc", "kyaeaaaaqgulcaaaaaaaaatamjqxaaaaa"))
    # print(cmp_hash("htsjfxnfqvxkwxy", "aoejroosriuwvqr"))
    # print(find_collision_fast(BASE, MODS))
    print(find_collision_rho())
    