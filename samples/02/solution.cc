/*
 * Author : wowoto9772
 * Date : 2016/12/28
 * Email : csjaj9772@gmail.com
 * Time Limit : 1 second
 * Memory Limit : 128 MB
 * Time Complexity : O(n log n)
 */

#include <cstdio>
#include <limits.h>

#include <vector>
#include <algorithm>

#define ll long long

using namespace std;

class segment {
public:
	// find interval's maximum consecutive sum
	int n;

	class ele {
	public:
		ll le, ri, mi, ans;
		ele() {}
		ele(ll a, ll b, ll c, ll d) {
			le = a, ri = b, mi = c, ans = d;
		}
	};

	bool eQuals(const ele &a, const ele &b) {
		return a.ans == b.ans && a.le == b.le && a.ri == b.ri && a.mi == b.mi;
	}

	ele minV;

	vector <ele> t;

	segment(vector <ll> &I) {
		n = I.size();
		t.resize(4 * n + 1);
		minV = { LLONG_MIN / 2, LLONG_MIN / 2, LLONG_MIN / 2, LLONG_MIN / 2 };
		init(I, 1, 0, n-1);
	}

	void init(vector <ll> &I, int x, int xl, int xr) {
		if (xl == xr) {
			t[x].le = t[x].ri = t[x].mi = t[x].ans = I[xl];
		}
		else {
			int m = (xl + xr) / 2;

			int le = x << 1;
			int ri = le + 1;

			init(I, le, xl, m);
			init(I, ri, m + 1, xr);

			t[x].ri = max(t[le].ri + t[ri].mi, t[ri].ri);
			t[x].le = max(t[le].mi + t[ri].le, t[le].le);
			t[x].mi = t[le].mi + t[ri].mi;
			t[x].ans = max({ t[le].ri + t[ri].le, t[le].ans, t[ri].ans, t[x].le, t[x].ri });
		}
	}

	ele query(int il, int ir, int x, int xl, int xr) {

		if (ir < xl || xr < il) {
			return minV;
		}
		else if (il <= xl && xr <= ir) {
			return t[x];
		}
		else {
			int m = (xl + xr) / 2;

			int _le = x << 1;
			int _ri = _le | 1;

			ele le = query(il, ir, _le, xl, m);
			ele ri = query(il, ir, _ri, m + 1, xr);

			ele ret;

			// validation
			if (eQuals(le, minV))ret = ri;
			else if (eQuals(ri, minV))ret = le;
			else {
				ret.le = max(le.le, le.mi + ri.le);
				ret.ri = max(ri.ri, ri.mi + le.ri);
				ret.mi = le.mi + ri.mi;
				ret.ans = max({ le.ri + ri.le, le.ans, ri.ans, ret.le, ret.ri });
			}

			return ret;
		}
	}

	ll query(int il, int ir) {
		return query(il, ir, 1, 0, n-1).ans;
	}
};



int main() {

	int n, q;
	scanf("%d %d", &n, &q);

	vector <ll> e(n);

	for (int i = 0; i < n; i++)scanf("%lld", &e[i]);

	segment tree(e);

	int v = 0;

	while (q--) {
		int le, ri;
		scanf("%d %d", &le, &ri);

		if (le > ri) {
			int k = le;
			le = ri;
			ri = k;
		}

		le--, ri--;

		printf("%lld\n", tree.query(le, ri));
	}

}
