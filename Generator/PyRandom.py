import random


def randInt(a, b):
    return random.randint(a, b)


def randBitInt(bits):
    return random.getrandbits(bits)


def randBit(bits):
    return bin(random.getrandbits(bits))[2:]


def randInRange(begin, end, step=1):
    ar = [value for value in range(begin, end, step)]
    random.shuffle(ar)
    return ar


def randCharLower():
    # a - z
    return chr(random.randint(97, 122))


def randChar():
    # a - z & A - Z
    c = [x for x in range(65, 91)] + [x for x in range(97, 123)]
    return chr(random.choice(c))


def Choice(array):
    return random.choice(array)


def Shuffle(array):
    random.shuffle(array)
