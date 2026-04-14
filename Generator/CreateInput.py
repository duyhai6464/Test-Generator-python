import sys
import random


def randInt(a, b):
    if int(a) > int(b): a, b = b, a
    return random.randint(int(a), int(b))


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
    n = randInt(5e3, 1e4)
    q = randInt(5e3, 1e4)
    print(n, q)
    for _ in range(q):
        query_type = randInt(0, 1) if _ != q - 1 else 1
        l = randInt(1, n)
        r = randInt(l, n)
        if query_type == 1:
            print(query_type, l, r)
        else:
            x = randInt(-1e3, 1e3)
            print(query_type, l, r, x)

def check_time_limit():
    n = randInt(1e5, 2e5)
    q = randInt(1e5, 2e5)
    print(n, q)
    for _ in range(q):
        query_type = randInt(0, 1) if _ != q - 1 else 1
        l = randInt(1, n // 10)
        r = randInt(9 * n // 10, n)
        if query_type == 1:
            print(query_type, l, r)
        else:
            x = randInt(-1e9, 1e9)
            print(query_type, l, r, x)

def hard_test_case():
    n = 2 * 10 ** 5
    q = 2 * 10 ** 5
    print(n, q)
    last_l, last_r = 1, n
    for _ in range(q):
        l = randInt(last_l, last_r)
        r = randInt(l, (l + n // 2) % n + 1)
        if l > r: l, r = r, l
        last_l, last_r = l, r
        if _ % 2:
            print(1, l, r)
        else:
            x = randInt(-1e9, 1e9)
            print(0, l, r, x)

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

test_case_index = 2
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
    
