/*
 * Author : wowoto9772
 * Date   : 2016/12/28
 * Email  : csjaj9772@gmail.com
 * Time Limit : 2 seconds
 * Memory Limit : 128 MB
 * Time Complexity : O(n^2 log (n^2))
 */

#include <cstdio>
#include <time.h>
#include <queue>
#include <vector>

using namespace std;

int meat[1003][1003];
bool chk[1003][1003];

int dr[] = { 0, 0, -1, 1 };
int dc[] = { -1, 1, 0, 0 };

class ele {
public:
	int r, c, v;
	ele() {}
	ele(int a, int b, int k) {
		r = a, c = b, v = k;
	}
	bool operator<(const ele &A)const {
		return v > A.v;
	}
};

int main() {

	int r, c;

	scanf("%d %d", &r, &c);

	for (int i = 1; i <= r; i++) {
		for (int j = 1; j <= c; j++) {
			scanf("%d", &meat[i][j]);
		}
	}

	priority_queue <ele> q;
	q.emplace(1, 1, meat[1][1]);

	while (!q.empty()) {
		ele f = q.top(); q.pop();
		if (chk[f.r][f.c])continue;
		if (f.r == r && f.c == c) {
			printf("%d\n", f.v);
			break;
		}
		chk[f.r][f.c] = true;
		for (int i = 0; i < 4; i++) {
			ele g = { f.r + dr[i], f.c + dc[i], f.v };
			g.v += meat[g.r][g.c];
			if (g.r < 1 || g.c < 1 || g.r > r || g.c > c)continue;
			if (!chk[g.r][g.c]) {
				q.emplace(g);
			}
		}
	}

}
