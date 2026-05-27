#include <bits/stdc++.h>
using namespace std;

struct Fenwick {
    int n = 0;
    vector<long long> bit;

    Fenwick() = default;
    explicit Fenwick(int n_) { init(n_); }

    void init(int n_) {
        n = n_;
        bit.assign(n + 1, 0);
    }

    void add(int idx, long long val) {
        for (; idx <= n; idx += idx & -idx) bit[idx] += val;
    }

    long long sumPrefix(int idx) const {
        long long res = 0;
        for (; idx > 0; idx -= idx & -idx) res += bit[idx];
        return res;
    }

    long long rangeSum(int l, int r) const {
        return sumPrefix(r) - sumPrefix(l - 1);
    }

    int kth(long long k) const {
        int idx = 0;
        int step = 1;
        while ((step << 1) <= n) step <<= 1;

        for (; step; step >>= 1) {
            int nxt = idx + step;
            if (nxt <= n && bit[nxt] < k) {
                idx = nxt;
                k -= bit[nxt];
            }
        }
        return idx + 1;
    }
};

struct SegmentMin {
    static constexpr int INF = 1'000'000'000;

    int n = 0;
    int base = 1;
    vector<int> mn;

    SegmentMin() = default;
    explicit SegmentMin(const vector<int>& pos) { build(pos); }

    void build(const vector<int>& pos) {
        n = (int)pos.size() - 1;
        base = 1;
        while (base < n) base <<= 1;
        mn.assign(base << 1, INF);

        for (int value = 1; value <= n; ++value) {
            mn[base + value - 1] = pos[value];
        }
        for (int node = base - 1; node >= 1; --node) {
            mn[node] = min(mn[node << 1], mn[node << 1 | 1]);
        }
    }

    void update(int value, int newPos) {
        int node = base + value - 1;
        mn[node] = newPos;
        for (node >>= 1; node; node >>= 1) {
            mn[node] = min(mn[node << 1], mn[node << 1 | 1]);
        }
    }

    int firstAtMostPos(int leftValue, int limitPos) const {
        if (leftValue > n || mn[1] > limitPos) return -1;
        return firstRec(1, 1, base, leftValue, n, limitPos);
    }

    int lastAtMostPos(int rightValue, int limitPos) const {
        if (rightValue < 1 || mn[1] > limitPos) return -1;
        return lastRec(1, 1, base, 1, rightValue, limitPos);
    }

    int firstRec(int node, int lo, int hi, int ql, int qr, int limitPos) const {
        if (hi < ql || qr < lo || mn[node] > limitPos) return -1;
        if (lo == hi) return lo <= n ? lo : -1;

        int mid = (lo + hi) >> 1;
        int res = firstRec(node << 1, lo, mid, ql, qr, limitPos);
        if (res != -1) return res;
        return firstRec(node << 1 | 1, mid + 1, hi, ql, qr, limitPos);
    }

    int lastRec(int node, int lo, int hi, int ql, int qr, int limitPos) const {
        if (hi < ql || qr < lo || mn[node] > limitPos) return -1;
        if (lo == hi) return lo <= n ? lo : -1;

        int mid = (lo + hi) >> 1;
        int res = lastRec(node << 1 | 1, mid + 1, hi, ql, qr, limitPos);
        if (res != -1) return res;
        return lastRec(node << 1, lo, mid, ql, qr, limitPos);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;

    vector<int> f(n + 1);
    vector<string> initial;
    initial.reserve(n);

    char pendingType = 0;
    for (int i = 0; i < n; ++i) {
        string token;
        cin >> token;
        if (token.size() == 1 && (token[0] == '+' || token[0] == '-' || token[0] == '?')) {
            pendingType = token[0];
            break;
        }
        initial.push_back(token);
    }

    if ((int)initial.size() == n) {
        for (int i = 1; i <= n; ++i) f[i] = stoi(initial[i - 1]);
    } else {
        f[1] = 0;
        for (int i = 2; i <= n; ++i) f[i] = stoi(initial[i - 2]);
    }

    vector<int> p(n + 1), pos(n + 1);
    Fenwick alive(n);
    for (int value = 1; value <= n; ++value) alive.add(value, 1);

    for (int i = n; i >= 1; --i) {
        int value = alive.kth(f[i] + 1LL);
        p[i] = value;
        pos[value] = i;
        alive.add(value, -1);
    }

    Fenwick sum(n);
    for (int i = 1; i <= n; ++i) sum.add(i, p[i]);

    SegmentMin seg(pos);
    string answer;
    answer.reserve((size_t)q * 12);

    while (q--) {
        char type;
        if (pendingType) {
            type = pendingType;
            pendingType = 0;
        } else {
            cin >> type;
        }

        if (type == '?') {
            int l, r;
            cin >> l >> r;
            answer += to_string(sum.rangeSum(l, r));
            answer += '\n';
            continue;
        }

        int i;
        cin >> i;

        int x = p[i];
        int y = (type == '+')
                    ? seg.firstAtMostPos(x + 1, i)
                    : seg.lastAtMostPos(x - 1, i);

        int k = pos[y];
        p[i] = y;
        p[k] = x;
        pos[x] = k;
        pos[y] = i;

        sum.add(i, (long long)y - x);
        sum.add(k, (long long)x - y);

        seg.update(x, k);
        seg.update(y, i);
    }

    cout << answer;
    return 0;
}
