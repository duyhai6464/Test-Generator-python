class BIT: # by domigo
    def __init__(self, size):
        self.size = size
        self.bit = [0] * (size + 1)

    def add(self, idx, val):
        while idx <= self.size:
            self.bit[idx] += val
            idx += idx & -idx

    def prefix(self, idx):
        s = 0
        while idx > 0:
            s += self.bit[idx]
            idx ^= idx & -idx
        return s
    
    def query(self, l, r):
        if l > r: return 0
        return self.prefix(r) - self.prefix(l - 1)