import sys
import random


def rand(a, b=None):
    if b == None:
        a, b = 0, a
    if int(a) > int(b): a, b = int(b), int(a)
    return random.randint(a, b)


def randBitInt(bits):
    return random.getrandbits(int(bits))


def randBit(bits):
    return bin(random.getrandbits(int(bits)))[2:]


def randInRange(begin, end, step=1):
    if (int(begin) - int(end)) * int(step) > 0:
        begin, end = end, begin
    ar = [value for value in range(int(begin), int(end), int(step))]
    random.shuffle(ar)
    return ar


def randCharLower():
    # char to int: ord('a') = 97, ord('z') = 122
    return chr(random.randint(ord('a'), ord('z')))


def randChar():
    # a - z & A - Z
    c = [x for x in range(ord('A'), ord('Z') + 1)] + [x for x in range(ord('a'), ord('z') + 1)]
    return chr(random.choice(c))


def Choice(array):
    return random.choice(array)


def Shuffle(array):
    random.shuffle(array)
    return array


def example():
    n = rand(5e3, 1e4)
    q = rand(5e3, 1e4)
    print(n, q)
    for _ in range(q):
        query_type = rand(0, 1) if _ != q - 1 else 1
        l = rand(1, n)
        r = rand(l, n)
        if query_type == 1:
            print(query_type, l, r)
        else:
            x = rand(-1e3, 1e3)
            print(query_type, l, r, x)

def check_time_limit():
    n = rand(1e5, 2e5)
    q = rand(1e5, 2e5)
    print(n, q)
    for _ in range(q):
        query_type = rand(0, 1) if _ != q - 1 else 1
        l = rand(1, n // 10)
        r = rand(9 * n // 10, n)
        if query_type == 1:
            print(query_type, l, r)
        else:
            x = rand(-1e9, 1e9)
            print(query_type, l, r, x)

def hard_test_case():
    n = int(2e5)
    q = int(2e5)
    print(n, q)
    for _ in range(q):
        query_type = 0 if _ % 2 else 1
        l = rand(1, n // 10)
        r = rand(9 * n // 10, n)
        if query_type == 1:
            print(query_type, l, r)
        else:
            x = rand(-1e9, 1e9)
            print(query_type, l, r, x)
        

def generate_test_cases(func):
    """
    first line is n, q (1 <= n, q <= 2*10^5) n integers of the array a initially 0
    next q lines are queries of the form "sum l r" or "add l r x"
    where l, r are the range of the query (1 <= l <= r <= n) and x is the value to add (-10^9 <= x <= 10^9)
     - "1 l r" means to calculate the sum of the subarray a[l...r]
     - "0 l r x" means to add x to each element in the subarray a[l...r]
    """
    filename = f'{test_case_index}.in'
    with open('test/' + filename, 'w') as FileOutput:
        print(f'Generating test case {test_case_index}...{filename}')
        sys.stdout = FileOutput
        func()# Generate the test case
        sys.stdout = sys.__stdout__

def generate_input(func, genpath):
    with open(genpath, 'w') as FileOutput:
        print(f'Generating input to {genpath}.')
        sys.stdout = FileOutput
        func()# Generate the test case
        sys.stdout = sys.__stdout__

def sample_test():
    for _ in range(10):
        n = 10
        print(n)
        print(' '.join(map(str, [rand(1, 10) for _ in range(n)])))
        print(' '.join(map(str, [rand(1, 10) for _ in range(n)])))
        print(rand(n * 5, n * 10))
        print("EOF")


test_case_index = 100
if __name__ == '__main__':
    while test_case_index < 3:
        generate_test_cases(example)
        test_case_index += 1
    while test_case_index < 5:
        generate_test_cases(check_time_limit)
        test_case_index += 1
    while test_case_index < 7:
        generate_test_cases(hard_test_case)
        test_case_index += 1
    generate_input(sample_test, 'gen.in')
    # generate_input(sample_test_out, 'gen.out')
