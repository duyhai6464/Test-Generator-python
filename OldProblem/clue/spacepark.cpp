#include <bits/stdc++.h>
using namespace std;

using int64 = long long;
using i128 = __int128_t;

vector<int64> a;

template <int CAP>
struct Node {
    int sz = 0;
    array<int, CAP> id{};
};

using MinNode = Node<2>;
using MaxNode = Node<3>;

static inline void addMin(MinNode &res, int idx) {
    for (int i = 0; i < res.sz; ++i) {
        if (res.id[i] == idx) return;
    }

    int pos = 0;
    while (pos < res.sz && a[res.id[pos]] <= a[idx]) {
        ++pos;
    }
    if (pos == 2) return;

    if (res.sz < 2) {
        ++res.sz;
    }
    for (int k = res.sz - 1; k > pos; --k) {
        res.id[k] = res.id[k - 1];
    }
    res.id[pos] = idx;
}

static inline void addMax(MaxNode &res, int idx) {
    for (int i = 0; i < res.sz; ++i) {
        if (res.id[i] == idx) return;
    }

    int pos = 0;
    while (pos < res.sz && a[res.id[pos]] >= a[idx]) {
        ++pos;
    }
    if (pos == 3) return;

    if (res.sz < 3) {
        ++res.sz;
    }
    for (int k = res.sz - 1; k > pos; --k) {
        res.id[k] = res.id[k - 1];
    }
    res.id[pos] = idx;
}

static inline MinNode mergeMin(const MinNode &x, const MinNode &y) {
    MinNode res;
    for (int i = 0; i < x.sz; ++i) addMin(res, x.id[i]);
    for (int i = 0; i < y.sz; ++i) addMin(res, y.id[i]);
    return res;
}

static inline MaxNode mergeMax(const MaxNode &x, const MaxNode &y) {
    MaxNode res;
    for (int i = 0; i < x.sz; ++i) addMax(res, x.id[i]);
    for (int i = 0; i < y.sz; ++i) addMax(res, y.id[i]);
    return res;
}

static string toString(i128 x) {
    if (x == 0) return "0";

    bool neg = x < 0;
    if (neg) x = -x;

    string s;
    while (x > 0) {
        s.push_back(char('0' + x % 10));
        x /= 10;
    }
    if (neg) s.push_back('-');
    reverse(s.begin(), s.end());
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, t;
    cin >> n >> t;

    a.resize(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }

    vector<int> lg(n + 1, 0);
    for (int i = 2; i <= n; ++i) {
        lg[i] = lg[i / 2] + 1;
    }

    int levels = lg[n] + 1;
    vector<vector<MinNode>> stMin(levels);
    vector<vector<MaxNode>> stMax(levels);

    stMin[0].resize(n);
    stMax[0].resize(n);
    for (int i = 0; i < n; ++i) {
        stMin[0][i].sz = 1;
        stMin[0][i].id[0] = i;
        stMax[0][i].sz = 1;
        stMax[0][i].id[0] = i;
    }

    for (int j = 1; j < levels; ++j) {
        int len = 1 << j;
        int half = len >> 1;
        int size = n - len + 1;

        stMin[j].resize(size);
        stMax[j].resize(size);
        for (int i = 0; i < size; ++i) {
            stMin[j][i] = mergeMin(stMin[j - 1][i], stMin[j - 1][i + half]);
            stMax[j][i] = mergeMax(stMax[j - 1][i], stMax[j - 1][i + half]);
        }
    }

    auto queryMin = [&](int l, int r) {
        int j = lg[r - l + 1];
        int len = 1 << j;
        return mergeMin(stMin[j][l], stMin[j][r - len + 1]);
    };

    auto queryMax = [&](int l, int r) {
        int j = lg[r - l + 1];
        int len = 1 << j;
        return mergeMax(stMax[j][l], stMax[j][r - len + 1]);
    };

    while (t--) {
        int l, r;
        cin >> l >> r;
        --l;
        --r;

        MinNode mi = queryMin(l, r);
        MaxNode ma = queryMax(l, r);

        vector<int> ids;
        auto pushUnique = [&](int idx) {
            for (int cur : ids) {
                if (cur == idx) return;
            }
            ids.push_back(idx);
        };

        for (int i = 0; i < mi.sz; ++i) pushUnique(mi.id[i]);
        for (int i = 0; i < ma.sz; ++i) pushUnique(ma.id[i]);

        sort(ids.begin(), ids.end(), [](int x, int y) {
            return a[x] < a[y];
        });

        int m = (int)ids.size();
        i128 ans = (i128)a[ids[0]] * a[ids[1]] * a[ids[m - 1]];
        ans = max(ans, (i128)a[ids[m - 1]] * a[ids[m - 2]] * a[ids[m - 3]]);

        cout << toString(ans) << '\n';
    }

    return 0;
}
