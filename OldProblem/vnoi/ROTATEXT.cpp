#include <bits/stdc++.h>

using namespace std;

struct Fenwick
{
    int n = 0;
    int mod = 1;
    vector<int> bit;

    Fenwick() = default;
    Fenwick(int n_, int mod_) : n(n_), mod(mod_), bit(n_ + 2, 0) {}

    void addPoint(int idx, int value)
    {
        for (; idx <= n; idx += idx & -idx)
        {
            bit[idx] += value;
            bit[idx] %= mod;
        }
    }

    void addRange(int left, int right, int value)
    {
        if (value == 0)
        {
            return;
        }
        addPoint(left, value);
        if (right + 1 <= n)
        {
            addPoint(right + 1, mod - value);
        }
    }

    int get(int idx) const
    {
        int result = 0;
        for (; idx > 0; idx -= idx & -idx)
        {
            result += bit[idx];
            result %= mod;
        }
        return result;
    }
};

struct SegmentTree
{
    int n = 0;
    int mod = 1;
    uint32_t fullMask = 1;
    vector<uint32_t> mask;
    vector<int> lazy;

    SegmentTree() = default;

    SegmentTree(const vector<int> &diff, int mod_)
    {
        n = static_cast<int>(diff.size()) - 1;
        mod = mod_;
        fullMask = (1u << mod) - 1u;
        mask.assign(4 * n + 5, 0);
        lazy.assign(4 * n + 5, 0);
        build(1, 1, n, diff);
    }

    uint32_t rotateMask(uint32_t value, int shift) const
    {
        if (shift == 0)
        {
            return value;
        }
        return ((value << shift) | (value >> (mod - shift))) & fullMask;
    }

    void apply(int node, int shift)
    {
        if (shift == 0)
        {
            return;
        }
        mask[node] = rotateMask(mask[node], shift);
        lazy[node] += shift;
        lazy[node] %= mod;
    }

    void push(int node)
    {
        int shift = lazy[node];
        if (shift == 0)
        {
            return;
        }
        apply(node << 1, shift);
        apply(node << 1 | 1, shift);
        lazy[node] = 0;
    }

    void pull(int node)
    {
        mask[node] = mask[node << 1] | mask[node << 1 | 1];
    }

    void build(int node, int left, int right, const vector<int> &diff)
    {
        if (left == right)
        {
            mask[node] = 1u << diff[left];
            return;
        }
        int mid = (left + right) >> 1;
        build(node << 1, left, mid, diff);
        build(node << 1 | 1, mid + 1, right, diff);
        pull(node);
    }

    void update(int node, int start, int end, int left, int right, int shift)
    {
        if (end < left || right < start)
        {
            return;
        }
        if (left <= start && end <= right)
        {
            apply(node, shift);
            return;
        }
        push(node);
        int mid = (start + end) >> 1;
        update(node << 1, start, mid, left, right, shift);
        update(node << 1 | 1, mid + 1, end, left, right, shift);
        pull(node);
    }

    void update(int left, int right, int shift)
    {
        update(1, 1, n, left, right, shift);
    }

    int firstDifferent(int node, int start, int end, int lowerBound)
    {
        if (end < lowerBound || mask[node] == 1u)
        {
            return -1;
        }
        if (start == end)
        {
            return start;
        }
        push(node);
        int mid = (start + end) >> 1;
        int result = firstDifferent(node << 1, start, mid, lowerBound);
        if (result != -1)
        {
            return result;
        }
        return firstDifferent(node << 1 | 1, mid + 1, end, lowerBound);
    }

    int firstDifferent(int lowerBound)
    {
        return firstDifferent(1, 1, n, lowerBound);
    }

    int getDiff(int node, int start, int end, int index)
    {
        if (start == end)
        {
            return __builtin_ctz(mask[node]);
        }
        push(node);
        int mid = (start + end) >> 1;
        if (index <= mid)
        {
            return getDiff(node << 1, start, mid, index);
        }
        return getDiff(node << 1 | 1, mid + 1, end, index);
    }

    int getDiff(int index)
    {
        return getDiff(1, 1, n, index);
    }
};

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, c, q;
    string s, t;
    cin >> n >> c >> q >> s >> t;

    vector<int> initialS(n + 1), diff(n + 1);
    for (int i = 1; i <= n; ++i)
    {
        initialS[i] = s[i - 1] - 'a';
        int tValue = t[i - 1] - 'a';
        diff[i] = (initialS[i] - tValue + c) % c;
    }

    Fenwick sShift(n, c);
    SegmentTree diffTree(diff, c);

    string output;
    output.reserve(q * 2);

    while (q--)
    {
        int type;
        cin >> type;

        if (type == 3)
        {
            int left;
            cin >> left;

            int pos = diffTree.firstDifferent(left);
            if (pos == -1)
            {
                output += "=\n";
                continue;
            }

            int sValue = (initialS[pos] + sShift.get(pos)) % c;
            int tValue = (sValue - diffTree.getDiff(pos) + c) % c;
            output += (sValue < tValue ? '<' : '>');
            output += '\n';
            continue;
        }

        int left, right, shift;
        cin >> left >> right >> shift;
        shift %= c;
        if (shift == 0)
        {
            continue;
        }

        if (type == 1)
        {
            sShift.addRange(left, right, shift);
            diffTree.update(left, right, shift);
        }
        else
        {
            diffTree.update(left, right, c - shift);
        }
    }

    if (!output.empty())
    {
        output.pop_back();
    }
    cout << output;
    return 0;
}
