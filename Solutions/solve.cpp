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
template <typename type>
istream &operator>>(istream &in, vector<type> &a)
{
    for (int i = 0; i < a.size(); i++)
        in >> a[i];
    return in;
}
template <typename type>
ostream &operator<<(ostream &out, const vector<type> &a)
{
    for (int i = 0; i < a.size(); i++)
        out << a[i] << " ";
    return out;
}
template <typename t1, typename t2>
istream &operator>>(istream &in, pair<t1, t2> &a)
{
    in >> a.first >> a.second;
    return in;
}
bool Multitests = 1;
ll test = 1;

void Solve()
{
    ll n, b[2] = {0};
    cin >> n;
    vector<ll> a(n);
    cin >> a;
    sort(allr(a));
    for (int i = 0; i < n; i++)
        b[i % 2] += (a[i] % 2 == i % 2) ? a[i] : 0;

    if (b[0] > b[1])
        cout << "Aco";
    else if (b[0] < b[1])
        cout << "Kbich";
    else
        cout << "Tie";
    cout << endl;
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