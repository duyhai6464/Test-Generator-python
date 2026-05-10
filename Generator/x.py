import bisect, numpy

def is_c(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0: return False
    return True

# t = int(1e9+10) + 7000
# for i in range(50):
#     if is_c(i):
#         print(i, end=', ')

# p = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
# print(len(p))

# a = numpy.zeros((4, 2, 3), dtype=int)
a = numpy.array(range(24), dtype=int)
a = a.reshape((4, 2, 3))

print(a)
print()
print(a[1][1])
print(a[1][1][-1:])
print(a[1][1][:-1])
print(a[1][1][-1:] + a[1][1][:-1])