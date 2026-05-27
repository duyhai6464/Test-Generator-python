import sys

def debug(*x, **y): print(*x, file=sys.stderr, **y)

def run():
    print('first')
    A, B = [], []
    X, Y = 100, 100
    print(X, Y)
    A.append((X, Y))
    turn = 0
    while True:
        if turn:
            if len(A) <= 1:
                if (X - 1, Y - 1) in B or (X + 1, Y + 1) in B:
                    Y -= 1
                else:
                    Y += 1
                X += 1
                print(X, Y)
                A.append((X, Y))
            else:
                dx = A[1][0] - A[0][0]
                dy = A[1][1] - A[0][1]
                if (A[1][0] + dx, A[1][1] + dy) not in B:
                    print(A[1][0] + dx, A[1][1] + dy)
                else:
                    print(A[0][0] - dx, A[0][1] - dy)
                return
        else:
            u, v = list(map(int, input().split()))
            if u <= 0 or v <= 0:
                return
            B.append((u, v))
        turn ^= 1

run()