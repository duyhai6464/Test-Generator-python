import sys
from PyRandom import *

N = 15  # number of test cases


def example():
    print(3)
    print(4)
    print(5, 2, 7, 3)
    print(3)
    print(1, 2, 3)
    print(4)
    print(2, 2, 2, 2)


def easy():
    t = 10000
    print(t)
    for _ in range(t):
        n = randInt(1, 10)
        a = [randInt(1, 10) for i in range(n)]
        print(n)
        print(*a)


def medium():
    t = 100
    print(t)
    for _ in range(t):
        n = randInt(1000, 2000)
        a = [randInt(1000, 10000) for i in range(n)]
        print(n)
        print(*a)


def hard():
    t = randInt(1, 4)
    print(t)
    for _ in range(t):
        n = 200000 // t
        if _ == 0:
            a = [randInt(100000, 100100) for i in range(n)]
        elif _ == 1:
            a = [randInt(100000000, 1000000000) for i in range(n)]
        else:
            a = [3 if i < 2*n/5 else 2 for i in range(n)]
        print(n)
        print(*a)


if __name__ == '__main__':
    for n in range(N):
        with open('test/' + str(n + 1) + '.in', 'w') as FileOut:
            sys.stdout = FileOut
            if n == 0:
                example()
            elif n <= N/3:
                easy()
            elif n <= 2*N/3:
                medium()
            else:
                hard()
