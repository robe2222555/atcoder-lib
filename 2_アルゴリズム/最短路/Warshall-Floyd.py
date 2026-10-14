def LI(): return list(map(int, input().split()))
def II(): return int(input())
"""     全点対最短路問題
任意の頂点対 (i,j)について, i~jの最短路を求める

ワーシャルフロイド法 計算量 O(V^3)
d[k][i][j] := {0, ..., k} U {i, j} の頂点のみを通るときの,
				iからjへの最短路を求めるdp

アイデア：
	dp[k] がすべて求まっていると仮定したとき，
	dp[k+1][i][j] は:
		- 頂点 k+1 を経由する <=> dp[k][i][k+1] + dp[k][k+1][j]
		- 頂点 k+1 を経由しない <=> dp[k][i][j]
"""

INF=float("inf")
V, E=LI()
# 始点，終点，コスト
Edge=[LI() for _ in range(E)]
d=[[INF]*V for _ in range(V)]
for i in range(V):
	d[i][i]=0
# 有向グラフだが，無向でも可
for s,t,cost in Edge:
	d[s][t]=cost

def WarshallFloyd():
	for k in range(V):
		for i in range(V):
			for j in range(V):
				d[i][j]=min(d[i][j], d[i][k]+d[k][j])

	return d
print(WarshallFloyd())

"""出力例(負の閉路あり)
[[0,   2,   4,   4, 8,   6],
[inf, 0,   2,   7, 6,   4],
[inf, inf, -1,  4, 3,   1],
[inf, inf, inf, 0, inf, inf],
[inf, inf, -5,  0, -1,  -3],
[inf, inf, -4,  1, 0,   -2]]

負の閉路があるかどうか＝マイナスの値がある
到達できない頂点対=inf

"""