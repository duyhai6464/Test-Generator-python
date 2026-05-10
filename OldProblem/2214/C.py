# RXOEARDMTINHUSERMEDESIANT & 20260401
# s = "RXOEARDMTINHUSERMEDESIANT"
# v = 20260401
# bit_v = bin(v)[2:]
# # bit_v same length as s, so we can use it to determine which characters in s to keep
# decode_s = ''.join([s[i] for i in range(len(s)) if bit_v[i] == '1'])
# print(decode_s)
# # output: "READTHEREST"
# # so we need check bit == 0

# decode_s = ''.join([s[i] for i in range(len(s)) if bit_v[i] == '0'])
# print(decode_s)# output: "XORMINUSMEDIAN"

t = int(input())
for _ in range(t):
    a = list(map(int, input().split()))
    res = 0
    for x in a:
        res ^= x
    print(res - sorted(a)[len(a) // 2])
    