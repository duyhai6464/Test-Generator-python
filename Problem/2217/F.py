import sys

data = list(map(int, sys.stdin.read().split()))
ptr = 0
out = []

def read():
    global ptr
    if ptr >= len(data):
        raise Exception("No more input")
    res = data[ptr]
    ptr += 1
    return res


def pre_run():
    pass

def run():
    x1, x2 = read(), read()

pre_run()
t = read()
for _ in range(t):
    out.append(str(run()))
    
sys.stdout.write("\n".join(out))