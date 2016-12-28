/*
 * Author : wowoto9772
 * Date : 2016/12/28
 * Email  : csjaj9772@gmail.com
 * Time Limit : 1 second
 * Memory Limit : 128 MB
 * Time Complexity : O(12 * n)
 */

#include <cstdio>
#include <cstring>
#include <algorithm>

using namespace std;

char jen[] = "wowotootowow"; // len : 12
int l = 12;
char str[300003];
int s;
int dp[300003][13];

int dy(int c, int m) {
	if (c == s) {
		return l - m;
	}
	else if (m == l) {
		return s - c;
	}

	if (dp[c][m] != -1)return dp[c][m];

	if (str[c] == jen[m]) {
		// nice
		dp[c][m] = dy(c + 1, m + 1);
	}
	else {
		// alter
		dp[c][m] = 1 + dy(c + 1, m + 1);
		// add
		dp[c][m] = min(dp[c][m], 1 + dy(c, m + 1));
		// remove
		dp[c][m] = min(dp[c][m], 1 + dy(c + 1, m));
	}

	return dp[c][m];
}

int main() {

	while (scanf("%s", str) == 1) {
		s = strlen(str);
		for (int i = 0; i < s; i++)for (int j = 0; j < 12; j++)dp[i][j] = -1;
		printf("%d\n", dy(0, 0));
	}

}
