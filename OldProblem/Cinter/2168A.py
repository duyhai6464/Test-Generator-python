# a-z 0-25 (z is space) we use 0-24
def int2str(v):
    s = []
    while v > 0:
        s.append(ord('a') + v % 25)
        v //= 25
    s.reverse()
    return ''.join(chr(c) for c in s)

def str2int(s):
    v = 0
    for c in s:
        v *= 25
        v += ord(c) - ord('a')
    return v

def run1():
    n = int(input())
    a = list(map(int, input().split()))
    ss = 'z'.join(int2str(v) for v in a)
    print(ss)

def run2():
    ss = input().split('z')
    print(len(ss))
    print(' '.join(str(str2int(s)) for s in ss))

s = input()
if s == "first":
    run1()
else:
    run2()