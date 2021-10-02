import sys
from PyRandom import *

N = 15  # number of test cases


def example():
    print(1)
    print(3, 4)


def easy():
    n = randInt(2, 4)
    print(n)
    for _ in range(n):
        print(randInt(10, 100), randInt(10, 100))


def medium():
    n = randInt(10, 100)
    print(n)
    for _ in range(n):
        print(randInt(100, 1000), randInt(100, 1000))


def hard():
    n = 1000
    print(n)
    for _ in range(n):
        print(randInt(1000000, 1000000000), randInt(1000000, 1000000000))


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
