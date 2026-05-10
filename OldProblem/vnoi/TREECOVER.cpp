#include <bits/stdc++.h>
using namespace std;

struct FastIO {
    static const int SZ = 1 << 20;
    int in_pos = 0, in_len = 0, out_len = 0;
    char in_buf[SZ], out_buf[SZ];

    ~FastIO() { flush(); }

    char get_char() {
        if (in_pos == in_len) {
            in_len = fread(in_buf, 1, SZ, stdin);
            in_pos = 0;
            if (!in_len) return 0;
        }
        return in_buf[in_pos++];
    }

    int read_int() {
        char c = get_char();
        while (c <= ' ') c = get_char();

        int x = 0;
        while (c > ' ') {
            x = x * 10 + (c - '0');
            c = get_char();
        }
        return x;
    }

    void write_int(int x) {
        char s[12];
        int n = 0;
        do {
            s[n++] = char('0' + x % 10);
            x /= 10;
        } while (x);

        while (n--) put_char(s[n]);
        put_char('\n');
    }

    void put_char(char c) {
        if (out_len == SZ) flush();
        out_buf[out_len++] = c;
    }

    void flush() {
        if (out_len) {
            fwrite(out_buf, 1, out_len, stdout);
            out_len = 0;
        }
    }
};

struct Fenwick {
    int n, mask = 1;
    vector<int> bit;

    Fenwick(int n = 0) : n(n), bit(n + 1) {
        while ((mask << 1) <= n) mask <<= 1;
    }

    void add(int i, int v) {
        for (; i <= n; i += i & -i) bit[i] += v;
    }

    int sum(int i) const {
        int s = 0;
        for (; i; i -= i & -i) s += bit[i];
        return s;
    }

    int kth(int k) const {
        int i = 0;
        for (int step = mask; step; step >>= 1) {
            int nxt = i + step;
            if (nxt <= n && bit[nxt] < k) {
                i = nxt;
                k -= bit[nxt];
            }
        }
        return i + 1;
    }
};

struct ActiveSet {
    int n, blocks, non_empty = 0;
    vector<unsigned long long> bits;
    Fenwick fw;

    ActiveSet(int n = 0) : n(n), blocks((n + 63) >> 6), bits(blocks), fw(blocks) {}

    void add(int pos) {
        int b = (pos - 1) >> 6, off = (pos - 1) & 63;
        if (!bits[b]) {
            fw.add(b + 1, 1);
            ++non_empty;
        }
        bits[b] |= 1ULL << off;
    }

    void remove(int pos) {
        int b = (pos - 1) >> 6, off = (pos - 1) & 63;
        bits[b] &= ~(1ULL << off);
        if (!bits[b]) {
            fw.add(b + 1, -1);
            --non_empty;
        }
    }

    int first_pos() const {
        int b = fw.kth(1) - 1;
        return (b << 6) + __builtin_ctzll(bits[b]) + 1;
    }

    int last_pos() const {
        int b = fw.kth(non_empty) - 1;
        return (b << 6) + 64 - __builtin_clzll(bits[b]);
    }

    int next_pos(int pos) const {
        int idx = pos, b = idx >> 6, off = idx & 63;
        if (b >= blocks) return 0;

        if (b < blocks) {
            unsigned long long cur = bits[b] & (~0ULL << off);
            if (cur) return (b << 6) + __builtin_ctzll(cur) + 1;
        }

        int before = fw.sum(b + 1);
        if (before == non_empty) return 0;
        b = fw.kth(before + 1) - 1;
        return (b << 6) + __builtin_ctzll(bits[b]) + 1;
    }

    int prev_pos(int pos) const {
        int idx = pos - 2;
        if (idx < 0) return 0;

        int b = idx >> 6, off = idx & 63;
        unsigned long long mask = off == 63 ? ~0ULL : ((1ULL << (off + 1)) - 1);
        unsigned long long cur = bits[b] & mask;
        if (cur) return (b << 6) + 64 - __builtin_clzll(cur);

        int before = fw.sum(b);
        if (!before) return 0;
        b = fw.kth(before) - 1;
        return (b << 6) + 64 - __builtin_clzll(bits[b]);
    }
};

int main() {
    static FastIO io;
    int n = io.read_int();
    int t = io.read_int();

    vector<int> head(n + 1, -1), to(2 * max(0, n - 1)), nxt(2 * max(0, n - 1));
    int edges = 0;

    auto add_edge = [&](int u, int v) {
        to[edges] = v;
        nxt[edges] = head[u];
        head[u] = edges++;
    };

    for (int i = 1; i < n; ++i) {
        int u = io.read_int();
        int v = io.read_int();
        add_edge(u, v);
        add_edge(v, u);
    }

    vector<int> parent(n + 1), depth(n + 1), tin(n + 1), tout(n + 1), order(n + 1);
    vector<int> st;
    st.reserve(n);
    st.push_back(1);

    int timer = 0;
    while (!st.empty()) {
        int u = st.back();
        st.pop_back();

        tin[u] = tout[u] = ++timer;
        order[timer] = u;

        for (int e = head[u]; e != -1; e = nxt[e]) {
            int v = to[e];
            if (v == parent[u]) continue;
            parent[v] = u;
            depth[v] = depth[u] + 1;
            st.push_back(v);
        }
    }

    for (int i = n; i > 1; --i) {
        int u = order[i];
        int p = parent[u];
        if (tout[u] > tout[p]) tout[p] = tout[u];
    }

    int lg = 32 - __builtin_clz(n);
    int stride = n + 1;
    vector<int> up(lg * stride);

    for (int u = 1; u <= n; ++u) up[u] = parent[u];
    for (int i = 1; i < lg; ++i) {
        int base = i * stride;
        int prev = base - stride;
        for (int u = 1; u <= n; ++u) up[base + u] = up[prev + up[prev + u]];
    }

    auto ancestor = [&](int u, int v) {
        return tin[u] <= tin[v] && tin[v] <= tout[u];
    };

    auto child_below = [&](int u, int x) {
        int diff = depth[x] - depth[u] - 1;
        for (int i = 0; diff; ++i, diff >>= 1) {
            if (diff & 1) x = up[i * stride + x];
        }
        return x;
    };

    ActiveSet active_pos(n);
    vector<unsigned char> active(n + 1), leaf(n + 1);
    int active_count = 0, leaf_count = 0;

    auto prev_node = [&](int pos) {
        int p = active_pos.prev_pos(pos);
        return order[p ? p : active_pos.last_pos()];
    };

    auto next_node = [&](int pos) {
        int p = active_pos.next_pos(pos);
        return order[p ? p : active_pos.first_pos()];
    };

    auto check_leaf = [&](int u, int pre, int nxt_node) {
        if (active_count <= 2) return true;

        bool in_pre = ancestor(u, pre);
        bool in_next = ancestor(u, nxt_node);
        if (!in_pre && !in_next) return true;
        if (in_pre != in_next) return false;
        return child_below(u, pre) == child_below(u, nxt_node);
    };

    auto set_leaf = [&](int u, bool now) {
        if (now != leaf[u]) {
            leaf_count += now ? 1 : -1;
            leaf[u] = (unsigned char)now;
        }
    };

    while (t--) {
        int u = io.read_int();
        int pos = tin[u];

        if (active[u]) {
            int total = active_count;
            int pre = 0, nxt_node = 0, pre2 = 0, nxt2 = 0;

            if (total > 1) {
                pre = prev_node(pos);
                nxt_node = next_node(pos);
                if (total > 3) {
                    pre2 = prev_node(tin[pre]);
                    nxt2 = next_node(tin[nxt_node]);
                }
            }

            leaf_count -= leaf[u];
            leaf[u] = active[u] = 0;
            --active_count;
            active_pos.remove(pos);

            if (active_count == 1) {
                set_leaf(pre, true);
            } else if (active_count == 2) {
                set_leaf(pre, true);
                set_leaf(nxt_node, true);
            } else if (active_count > 2) {
                set_leaf(pre, check_leaf(pre, pre2, nxt_node));
                set_leaf(nxt_node, check_leaf(nxt_node, pre, nxt2));
            }
        } else {
            active[u] = 1;
            ++active_count;
            active_pos.add(pos);

            if (active_count == 1) {
                set_leaf(u, true);
            } else if (active_count == 2) {
                int other = prev_node(pos);
                set_leaf(u, true);
                set_leaf(other, true);
            } else {
                int pre = prev_node(pos);
                int nxt_node = next_node(pos);
                int pre2 = prev_node(tin[pre]);
                int nxt2 = next_node(tin[nxt_node]);

                set_leaf(u, check_leaf(u, pre, nxt_node));
                set_leaf(pre, check_leaf(pre, pre2, u));
                set_leaf(nxt_node, check_leaf(nxt_node, u, nxt2));
            }
        }

        io.write_int((leaf_count + 1) >> 1);
    }

    return 0;
}
