#include <bits/stdc++.h>
#define author "CODE BY KQamazing"
#define faster                    \
    ios_base::sync_with_stdio(0); \
    cin.tie();                    \
    cout.tie()
#define ll long long
#define ld long double
#define pii pair<int, int>
#define pll pair<ll, ll>
#define pld pair<ld, ld>
#define matrix vector<vector<ll>>
#define all(_) _.begin(), _.end()
#define allr(_) _.rbegin(), _.rend()
#define Unique(_) _.erase(unique(all(_)), _.end());
#define Modd (ll)(1e9 + 7)

using namespace std;

bool Multitests = 1;
ll test = 1, n, m, k, l, r, x, y;

void Solve()
{
    cin >> n >> m;
    cout << n + m << endl;
}

int main()
{
    faster;

    if (Multitests)
        (cin >> test).ignore();
    while (test--)
        Solve();
    return 0;
}