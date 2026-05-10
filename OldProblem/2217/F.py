import sys

data = list(map(int, sys.stdin.read().split()))
ptr = 0
out = []

def read():
    global ptr
    if ptr >= len(data):
        raise Exception("No more input")
    _res = data[ptr]
    ptr += 1
    return _res


def run():
    x1, x2 = read(), read()
    # Đặt A = (l_1 - 1) ^ (x_1 - r_1) (Số Alice chọn) và B = (l_2 - 1) ^ (x_2 - r_2) (Số Bob chọn)
    if x1 > x2:
        return f"{x2 + 1} {x1}"
    best_A = 0
    min_f = 10**18
    for A in range(x1):
        # Alice đã chọn $A$, nên ta cần đếm số cặp $(u, v)$ sao cho u ^ v = A và u + v <= x_2 - 1
        # u + v = (u ^ v) + 2(u & v) = A + 2(u & v) <= x_2 - 1
        # ==> u & v <= (x_2 - 1 - A) // 2
        n = (x2 - 1 - A) // 2
        if n < 0:
            return f"{1} {x1}"
        temp_n = n
        res = 0
        while temp_n > 0:
            # Lấy bit cao nhất của n đang xét
            high_bit_idx = temp_n.bit_length() - 1
            bit_val = 1 << high_bit_idx
            
            # Nếu ta chọn bit này là 0 thay vì 1 (giống n)
            # thì các bit thấp hơn có thể chọn tự do miễn là (bit & A) == 0
            free_bits_below = high_bit_idx - popcounts[A & (bit_val - 1)]
            res += pow2[free_bits_below]
            
            # Để tiếp tục khớp với prefix của n (chọn bit này là 1)
            # thì A tại bit này bắt buộc phải là 0
            if A & bit_val:
                temp_n = -1 # Đánh dấu dừng (không khớp được prefix nữa)
                break
            temp_n ^= bit_val # Bỏ bit cao nhất để xét tiếp
        
        if temp_n == 0: # n thỏa mãn điều kiện (n & A == 0)
            res += 1
        
        cur_f = pow2[popcounts[A]] * res
        if cur_f <= min_f:
            min_f = cur_f
            best_A = A
            if min_f == 0: # tối ưu nhất có thể là 0, không cần tìm tiếp
                return f"{best_A + 1} {x1}"
    return f"{best_A + 1} {x1}"

# Precompute: Tính trước popcount và lũy thừa 2 để tăng tốc
# 2^19 > 500,000 nên chỉ cần đến 20 bits
MAX_VAL = 500005
popcounts = [0] * (MAX_VAL + 1)
for i in range(1, MAX_VAL + 1):
    popcounts[i] = popcounts[i >> 1] + (i & 1)

pow2 = [1] * 22
for i in range(1, 22):
    pow2[i] = pow2[i-1] * 2
t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))

