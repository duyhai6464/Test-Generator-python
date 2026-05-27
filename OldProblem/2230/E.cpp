#include <bits/stdc++.h>
using namespace std;

struct FastScanner {
    static constexpr int BUFFER_SIZE = 1 << 20;
    int idx = 0, size = 0;
    char buffer[BUFFER_SIZE];

    inline char get_char() {
        if (idx >= size) {
            size = (int)fread(buffer, 1, BUFFER_SIZE, stdin);
            idx = 0;
            if (size == 0) return 0;
        }
        return buffer[idx++];
    }

    int next_int() {
        char ch = get_char();
        while (ch && (ch < '0' || ch > '9')) ch = get_char();

        int value = 0;
        while (ch >= '0' && ch <= '9') {
            value = value * 10 + (ch - '0');
            ch = get_char();
        }
        return value;
    }
};

int main() {
    FastScanner fs;

    int n = fs.next_int();
    vector<int> p_values(n);
    for (int &x : p_values) x = fs.next_int();

    vector<pair<int, int>> points(n);
    for (int i = 0; i < n; ++i) {
        points[i] = {p_values[i], fs.next_int()};
    }

    sort(points.begin(), points.end());

    const int INF = 1'000'000'000;
    vector<int> p_front;
    vector<int> c_front;
    p_front.reserve(n);
    c_front.reserve(n);

    int best_c = INF;
    for (auto [p, c] : points) {
        if (c < best_c) {
            p_front.push_back(p);
            c_front.push_back(c);
            best_c = c;
        }
    }

    int k = (int)p_front.size();
    vector<int> logs(k + 1);
    for (int i = 2; i <= k; ++i) logs[i] = logs[i >> 1] + 1;

    int levels = logs[k] + 1;
    vector<vector<int>> sparse(levels, vector<int>(k));
    for (int i = 0; i < k; ++i) sparse[0][i] = p_front[i] + c_front[i];

    for (int level = 1; level < levels; ++level) {
        int len = 1 << level;
        int half = len >> 1;
        int usable = k - len + 1;
        for (int i = 0; i < usable; ++i) {
            sparse[level][i] = min(sparse[level - 1][i], sparse[level - 1][i + half]);
        }
    }

    vector<int> neg_c(k);
    for (int i = 0; i < k; ++i) neg_c[i] = -c_front[i];

    auto min_sum = [&](int left, int right) -> int {
        if (left >= right) return INF;
        int level = logs[right - left];
        int width = 1 << level;
        return min(sparse[level][left], sparse[level][right - width]);
    };

    auto count_c_ge = [&](int value) -> int {
        return (int)(upper_bound(neg_c.begin(), neg_c.end(), -value) - neg_c.begin());
    };

    auto has_common = [](int left_a, int right_a, int left_b, int right_b) -> bool {
        return max(left_a, left_b) < min(right_a, right_b);
    };

    auto best_const = [&](int left_a, int right_a, int left_b, int right_b, int value) -> int {
        return has_common(left_a, right_a, left_b, right_b) ? value : INF;
    };

    auto best_by_p = [&](int left_a, int right_a, int left_b, int right_b, int extra) -> int {
        int left = max(left_a, left_b);
        int right = min(right_a, right_b);
        return left < right ? p_front[left] + extra : INF;
    };

    auto best_by_c = [&](int left_a, int right_a, int left_b, int right_b, int extra) -> int {
        int left = max(left_a, left_b);
        int right = min(right_a, right_b);
        return left < right ? c_front[right - 1] + extra : INF;
    };

    auto best_by_sum = [&](int left_a, int right_a, int left_b, int right_b) -> int {
        int left = max(left_a, left_b);
        int right = min(right_a, right_b);
        return left < right ? min_sum(left, right) : INF;
    };

    auto solve_user = [&](int tp, int tc, int d) -> int {
        int p_mid = (int)(lower_bound(p_front.begin(), p_front.end(), tp) - p_front.begin());
        int p_full = (int)(lower_bound(p_front.begin(), p_front.end(), tp + d) - p_front.begin());

        int c_full = count_c_ge(tc + d);
        int c_mid = count_c_ge(tc);

        if (has_common(0, p_mid, c_mid, k)) return 0;

        int ans = INF;
        ans = min(ans, best_by_p(p_mid, p_full, c_mid, k, 0));
        ans = min(ans, best_const(p_full, k, c_mid, k, tp + d));
        ans = min(ans, best_by_c(0, p_mid, c_full, c_mid, 0));
        ans = min(ans, best_const(0, p_mid, 0, c_full, tc + d));
        ans = min(ans, best_by_sum(p_mid, p_full, c_full, c_mid));
        ans = min(ans, best_by_p(p_mid, p_full, 0, c_full, tc + d));
        ans = min(ans, best_by_c(p_full, k, c_full, c_mid, tp + d));
        ans = min(ans, best_const(p_full, k, 0, c_full, tp + tc + 2 * d));
        return ans;
    };

    int m = fs.next_int();
    vector<int> tp_values(m), tc_values(m);
    for (int &x : tp_values) x = fs.next_int();
    for (int &x : tc_values) x = fs.next_int();

    string output;
    output.reserve((size_t)m * 4);
    for (int i = 0; i < m; ++i) {
        int d = fs.next_int();
        output += to_string(solve_user(tp_values[i], tc_values[i], d));
        output += '\n';
    }

    fwrite(output.data(), 1, output.size(), stdout);
    return 0;
}
