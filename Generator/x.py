n, m = list(map(int, input().split()))
if n == 1:
    print(1)
else:
    W = list(map(int, input().split()))
    for i, w in enumerate(W, 1):
        if w==1:
            if m==0:
                print(i)
                break
            m-=1
    else:
        print(n)