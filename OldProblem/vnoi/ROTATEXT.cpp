#include <bits/stdc++.h>

using namespace std;

using int64 = long long;

struct FastScanner {
    static constexpr size_t BUFSIZE = 1 << 20;
    char buf[BUFSIZE];
    size_t idx = 0;
    size_t size = 0;

    inline char read() {
        if (idx >= size) {
            size = fread(buf, 1, BUFSIZE, stdin);
            idx = 0;
            if (size == 0) {
                return 0;
            }
        }
        return buf[idx++];
    }

    template <class T>
    bool nextInt(T &out) {
        char c;
        do {
            c = read();
            if (!c) {
                return false;
            }
        } while (c <= ' ');

        T sign = 1;
        if (c == '-') {
            sign = -1;
            c = read();
        }

        T value = 0;
        while (c > ' ') {
            value = value * 10 + (c - '0');
            c = read();
        }
        out = value * sign;
        return true;
    }

    bool nextString(string &out) {
        char c;
        do {
            c = read();
            if (!c) {
                return false;
            }
        } while (c <= ' ');

        out.clear();
        while (c > ' ') {
            out.push_back(c);
            c = read();
        }
        return true;
    }
};

static inline int64 mulMod(int64 a, int64 b, int64 mod) {
    return static_cast<int64>((__int128)a * b % mod);
}

static int64 powMod(int64 base, int64 exp, int64 mod) {
    int64 result = 1;
    while (exp > 0) {
        if (exp & 1LL) {
            result = mulMod(result, base, mod);
        }
        base = mulMod(base, base, mod);
        exp >>= 1LL;
    }
    return result;
}

struct Fenwick {
    int n = 0;
    int mod = 1;
    vector<int> bit;

    Fenwick() = default;
    Fenwick(int n_, int mod_) : n(n_), mod(mod_), bit(n_ + 2, 0) {}

    void addPoint(int idx, int value) {
        if (value == 0) {
            return;
        }
        for (; idx <= n; idx += idx & -idx) {
            bit[idx] += value;
            if (bit[idx] >= mod) {
                bit[idx] -= mod;
            }
        }
    }

    void addRange(int left, int right, int value) {
        if (value == 0) {
            return;
        }
        addPoint(left, value);
        if (right + 1 <= n) {
            addPoint(right + 1, mod - value);
        }
    }

    int prefix(int idx) const {
        int result = 0;
        for (; idx > 0; idx -= idx & -idx) {
            result += bit[idx];
            if (result >= mod) {
                result -= mod;
            }
        }
        return result;
    }
};

struct Solver {
    static constexpr int64 BASE = 911382323LL;
    static constexpr pair<int64, int64> MODS[27] = {
        {0, 0},
        {1000000007LL, 1000000009LL},
        {1000000007LL, 1000000009LL},
        {1000000009LL, 1000000021LL},
        {1000000009LL, 1000000021LL},
        {1000000021LL, 1000000181LL},
        {1000000009LL, 1000000021LL},
        {1000000009LL, 1000000093LL},
        {1000000009LL, 1000000033LL},
        {1000000009LL, 1000000207LL},
        {1000000021LL, 1000000181LL},
        {1000000123LL, 1000000321LL},
        {1000000009LL, 1000000021LL},
        {1000000093LL, 1000000223LL},
        {1000000009LL, 1000000093LL},
        {1000000021LL, 1000000321LL},
        {1000000033LL, 1000000097LL},
        {1000000181LL, 1000000453LL},
        {1000000009LL, 1000000207LL},
        {1000000021LL, 1000000097LL},
        {1000000021LL, 1000000181LL},
        {1000000009LL, 1000000093LL},
        {1000000123LL, 1000000321LL},
        {1000000349LL, 1000000579LL},
        {1000000009LL, 1000000033LL},
        {1000000801LL, 1000000901LL},
        {1000000093LL, 1000000223LL},
    };

    int n = 0;
    int c = 0;
    int q = 0;
    int64 mod1 = 0;
    int64 mod2 = 0;
    string s;
    string t;
    vector<int64> pow1, pow2, same1, same2, rot1, rot2;
    vector<int> initialS;
    vector<int64> h1, h2;
    vector<int> lazy;
    Fenwick bit;

    int decodeDelta(int64 x1, int64 x2) const {
        for (int d = 0; d < c; ++d) {
            if (rot1[d] == x1 && rot2[d] == x2) {
                return d;
            }
        }
        return 0;
    }

    int64 findRoot(int64 mod) const {
        if (c == 1) {
            return 1;
        }

        vector<int> factors;
        int value = c;
        for (int div = 2; div * div <= value; ++div) {
            if (value % div == 0) {
                factors.push_back(div);
                while (value % div == 0) {
                    value /= div;
                }
            }
        }
        if (value > 1) {
            factors.push_back(value);
        }

        const int64 step = (mod - 1) / c;
        for (int64 cand = 2;; ++cand) {
            int64 root = powMod(cand, step, mod);
            if (root == 1) {
                continue;
            }
            bool ok = true;
            for (int factor : factors) {
                if (powMod(root, c / factor, mod) == 1) {
                    ok = false;
                    break;
                }
            }
            if (ok) {
                return root;
            }
        }
    }

    void apply(int node, int shift) {
        if (shift == 0) {
            return;
        }
        h1[node] = mulMod(h1[node], rot1[shift], mod1);
        h2[node] = mulMod(h2[node], rot2[shift], mod2);
        lazy[node] += shift;
        if (lazy[node] >= c) {
            lazy[node] -= c;
        }
    }

    void push(int node) {
        int shift = lazy[node];
        if (shift == 0) {
            return;
        }
        int left = node << 1;
        apply(left, shift);
        apply(left | 1, shift);
        lazy[node] = 0;
    }

    void pull(int node, int rightLen) {
        int left = node << 1;
        int right = left | 1;
        h1[node] = (mulMod(h1[left], pow1[rightLen], mod1) + h1[right]) % mod1;
        h2[node] = (mulMod(h2[left], pow2[rightLen], mod2) + h2[right]) % mod2;
    }

    void build(int node, int left, int right, const vector<int> &diff) {
        if (left == right) {
            h1[node] = rot1[diff[left]];
            h2[node] = rot2[diff[left]];
            return;
        }

        int mid = (left + right) >> 1;
        int leftNode = node << 1;
        build(leftNode, left, mid, diff);
        build(leftNode | 1, mid + 1, right, diff);
        pull(node, right - mid);
    }

    void update(int node, int start, int end, int left, int right, int shift) {
        if (start > right || end < left) {
            return;
        }
        if (left <= start && end <= right) {
            apply(node, shift);
            return;
        }

        push(node);
        int mid = (start + end) >> 1;
        int leftNode = node << 1;
        update(leftNode, start, mid, left, right, shift);
        update(leftNode | 1, mid + 1, end, left, right, shift);
        pull(node, end - mid);
    }

    int getCurrentS(int index) const {
        int value = initialS[index] + bit.prefix(index);
        if (value >= c) {
            value -= c;
        }
        return value;
    }

    int compare(int node, int start, int end, int leftBound) {
        if (end < leftBound) {
            return 0;
        }

        int len = end - start + 1;
        if (leftBound <= start && h1[node] == same1[len] && h2[node] == same2[len]) {
            return 0;
        }

        if (start == end) {
            int delta = decodeDelta(h1[node], h2[node]);
            int sChar = getCurrentS(start);
            int tChar = sChar - delta;
            if (tChar < 0) {
                tChar += c;
            }
            return (sChar < tChar) ? -1 : 1;
        }

        push(node);
        int mid = (start + end) >> 1;
        int res = compare(node << 1, start, mid, leftBound);
        if (res != 0) {
            return res;
        }
        return compare(node << 1 | 1, mid + 1, end, leftBound);
    }

    void run() {
        FastScanner fs;
        fs.nextInt(n);
        fs.nextInt(c);
        fs.nextInt(q);
        fs.nextString(s);
        fs.nextString(t);

        tie(mod1, mod2) = MODS[c];
        pow1.assign(n + 1, 1);
        pow2.assign(n + 1, 1);
        same1.assign(n + 1, 0);
        same2.assign(n + 1, 0);
        for (int i = 1; i <= n; ++i) {
            pow1[i] = mulMod(pow1[i - 1], BASE, mod1);
            pow2[i] = mulMod(pow2[i - 1], BASE, mod2);
            same1[i] = (mulMod(same1[i - 1], BASE, mod1) + 1) % mod1;
            same2[i] = (mulMod(same2[i - 1], BASE, mod2) + 1) % mod2;
        }

        rot1.assign(c, 1);
        rot2.assign(c, 1);
        int64 root1 = findRoot(mod1);
        int64 root2 = findRoot(mod2);
        for (int i = 1; i < c; ++i) {
            rot1[i] = mulMod(rot1[i - 1], root1, mod1);
            rot2[i] = mulMod(rot2[i - 1], root2, mod2);
        }

        initialS.assign(n + 1, 0);
        vector<int> diff(n + 1, 0);
        for (int i = 1; i <= n; ++i) {
            int sValue = s[i - 1] - 'a';
            int tValue = t[i - 1] - 'a';
            initialS[i] = sValue;
            diff[i] = sValue - tValue;
            if (diff[i] < 0) {
                diff[i] += c;
            }
        }

        h1.assign((n << 2) + 5, 0);
        h2.assign((n << 2) + 5, 0);
        lazy.assign((n << 2) + 5, 0);
        bit = Fenwick(n, c);
        build(1, 1, n, diff);

        string out;
        out.reserve(static_cast<size_t>(q) * 2);
        for (int i = 0; i < q; ++i) {
            int type;
            fs.nextInt(type);
            if (type == 3) {
                int left;
                fs.nextInt(left);
                int cmp = compare(1, 1, n, left);
                out.push_back(cmp < 0 ? '<' : (cmp > 0 ? '>' : '='));
                out.push_back('\n');
                continue;
            }

            int left, right, shift;
            fs.nextInt(left);
            fs.nextInt(right);
            fs.nextInt(shift);
            shift %= c;
            if (shift == 0) {
                continue;
            }

            if (type == 1) {
                bit.addRange(left, right, shift);
                update(1, 1, n, left, right, shift);
            } else {
                update(1, 1, n, left, right, (c - shift) % c);
            }
        }

        if (!out.empty()) {
            out.pop_back();
        }
        fwrite(out.data(), 1, out.size(), stdout);
    }
};

constexpr pair<int64, int64> Solver::MODS[27];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    Solver solver;
    solver.run();
    return 0;
}
