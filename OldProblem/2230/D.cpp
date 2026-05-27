#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MAXN = 500005;

int count_t[4 * MAXN];
long long sum_L[4 * MAXN];
bool lazy_clear[4 * MAXN];
pair<int, int> intervals[MAXN];
int a[MAXN], b[MAXN];

void build(int node, int l, int r)
{
    count_t[node] = 0;
    sum_L[node] = 0;
    lazy_clear[node] = false;
    if (l == r)
        return;
    int mid = (l + r) / 2;
    build(2 * node, l, mid);
    build(2 * node + 1, mid + 1, r);
}

void push(int node)
{
    if (lazy_clear[node])
    {
        lazy_clear[2 * node] = true;
        count_t[2 * node] = 0;
        sum_L[2 * node] = 0;
        lazy_clear[2 * node + 1] = true;
        count_t[2 * node + 1] = 0;
        sum_L[2 * node + 1] = 0;
        lazy_clear[node] = false;
    }
}

void activate(int node, int l, int r, int idx)
{
    if (l == r)
    {
        count_t[node] = 1;
        sum_L[node] = idx;
        return;
    }
    push(node);
    int mid = (l + r) / 2;
    if (idx <= mid)
        activate(2 * node, l, mid, idx);
    else
        activate(2 * node + 1, mid + 1, r, idx);
    count_t[node] = count_t[2 * node] + count_t[2 * node + 1];
    sum_L[node] = sum_L[2 * node] + sum_L[2 * node + 1];
}

pair<long long, long long> query_and_clear(int node, int l, int r, int ql, int qr)
{
    if (ql > r || qr < l)
        return {0, 0};
    if (ql <= l && r <= qr)
    {
        pair<long long, long long> res = {count_t[node], sum_L[node]};
        count_t[node] = 0;
        sum_L[node] = 0;
        lazy_clear[node] = true;
        return res;
    }
    push(node);
    int mid = (l + r) / 2;
    auto res1 = query_and_clear(2 * node, l, mid, ql, qr);
    auto res2 = query_and_clear(2 * node + 1, mid + 1, r, ql, qr);
    count_t[node] = count_t[2 * node] + count_t[2 * node + 1];
    sum_L[node] = sum_L[2 * node] + sum_L[2 * node + 1];
    return {res1.first + res2.first, res1.second + res2.second};
}

void run_test_case()
{
    int n;
    cin >> n;
    for (int i = 1; i <= n; ++i)
        cin >> a[i];
    for (int i = 1; i <= n; ++i)
        cin >> b[i];

    build(1, 1, n);
    for (int i = 0; i <= n; ++i)
        intervals[i] = {-1, -1};

    long long ans = 0;

    for (int i = 1; i <= n; ++i)
    {
        if (intervals[0].first == -1)
        {
            intervals[0] = {i, i};
        }
        else
        {
            intervals[0].second = i;
        }
        activate(1, 1, n, i);

        if (a[i] == b[i])
        {
            int v = a[i];
            if (intervals[v - 1].first != -1)
            {
                if (intervals[v].first == -1)
                {
                    intervals[v] = intervals[v - 1];
                }
                else
                {
                    intervals[v].second = intervals[v - 1].second;
                }
                intervals[v - 1] = {-1, -1};
            }
        }
        else
        {
            int x = a[i] - 1;
            int y = b[i] - 1;
            if (intervals[x].first != -1)
            {
                auto res = query_and_clear(1, 1, n, intervals[x].first, intervals[x].second);
                ans += res.first * i - res.second;
            }
            if (intervals[y].first != -1)
            {
                auto res = query_and_clear(1, 1, n, intervals[y].first, intervals[y].second);
                ans += res.first * i - res.second;
            }
        }
    }

    auto res = query_and_clear(1, 1, n, 1, n);
    ans += res.first * (n + 1) - res.second;
    cout << ans << "\n";
}

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int multTestQ;
    if (cin >> multTestQ)
    {
        while (multTestQ--)
        {
            run_test_case();
        }
    }
    return 0;
}