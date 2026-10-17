# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/探索/Euler_tour/Euler_tour_subtree.py
# 参考: https://info.atcoder.jp/entry/algorithm_lectures/euler_tour_technique
# 部分木クエリだけのとき，pre-order のときにのみ tour に入れる
# u の部分木クエリは，[pre[u], post[u])
# 頂点番号は 1-indexed (1 ~ N)

from sys import setrecursionlimit
setrecursionlimit(10**8)

def Euler_tour(G, N, root=1):
	pre = [-1]*(N+1)
	post = [-1]*(N+1)
	par = [-1]*(N+1)
	sz = [1]*(N+1)
	tour = []
	def dfs(u, p=-1):
		pre[u] = len(tour)
		tour.append(u)
		for v in G[u]:
			if v==p: continue
			par[v] = u
			dfs(v, u)
			sz[u] += sz[v]
		post[u] = len(tour)
		return

	dfs(root)
	return pre, post, tour
