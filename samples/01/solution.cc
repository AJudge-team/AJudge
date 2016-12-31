/*
 * Author : wowoto9772
 * Date : 2016/12/28
 * Email : csjaj9772@gmail.com
 * Time Limit : 1 second
 * Memory Limit : 128 MB
 * Time Complexity : O(n)
*/

#include <cstdio>
using namespace std;

#define mod 3001

int dp[103];
bool spc[103];
int n;

int dy(int c) {
	if (c == n)return 1;
	else if (c > n)return 0;

	if (dp[c] != -1)return dp[c];
	
    dp[c] = 0;

	if (spc[c + 1] || spc[c + 2])dp[c] = dy(c + 1);
	else {
		dp[c] += dy(c + 2);
		dp[c] += dy(c + 1);
	}

	return dp[c] %= mod;
}

int main() {
	scanf("%d", &n);

	int m;
	scanf("%d", &m);

	while (m--) {
		int a;
		scanf("%d", &a);
		spc[a] = true;
	}

	for (int i = 0; i <= n; i++)dp[i] = -1;

	printf("%d\n", dy(0));
}
