#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

const int K_LIMIT = 12;
const int64 INF = (1LL << 62);

struct TopList
{
    array<int64, K_LIMIT> value{};
    int size = 0;
};

TopList merge_top(const TopList &left, const TopList &right)
{
    TopList res;
    int i = 0, j = 0;
    while (res.size < K_LIMIT && (i < left.size || j < right.size))
    {
        if (j == right.size || (i < left.size && left.value[i] >= right.value[j]))
        {
            res.value[res.size++] = left.value[i++];
        }
        else
        {
            res.value[res.size++] = right.value[j++];
        }
    }
    return res;
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, d;
    if (!(cin >> n >> d))
        return 0;

    vector<int64> a(n), pref(n + 1, 0);
    for (int i = 0; i < n; ++i)
    {
        cin >> a[i];
        pref[i + 1] = pref[i] + a[i];
    }

    int64 pow10[K_LIMIT + 1];
    pow10[0] = 1;
    for (int i = 1; i <= K_LIMIT; ++i)
    {
        if (pow10[i - 1] > INF / 10)
            pow10[i] = INF;
        else
            pow10[i] = pow10[i - 1] * 10;
    }

    int base = 1;
    while (base < n)
        base <<= 1;

    vector<TopList> tree(base << 1);
    for (int i = 0; i < n; ++i)
    {
        tree[base + i].size = 1;
        tree[base + i].value[0] = a[i];
    }
    for (int i = base - 1; i >= 1; --i)
    {
        tree[i] = merge_top(tree[i << 1], tree[i << 1 | 1]);
    }

    while (d--)
    {
        int l, r;
        cin >> l >> r;
        --l;
        --r;

        int64 total = pref[r + 1] - pref[l];
        int64 ans = total;

        TopList left_res, right_res;
        for (l += base, r += base; l <= r; l >>= 1, r >>= 1)
        {
            if (l & 1)
                left_res = merge_top(left_res, tree[l++]);
            if (!(r & 1))
                right_res = merge_top(tree[r--], right_res);
        }

        TopList top = merge_top(left_res, right_res);
        int64 remaining = total;
        for (int i = 0; i < top.size; ++i)
        {
            remaining -= top.value[i];
            ans = min(ans, remaining + pow10[i + 1]);
        }

        cout << ans << '\n';
    }

    return 0;
}
