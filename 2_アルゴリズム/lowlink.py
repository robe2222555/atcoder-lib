# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/lowlink.py
# 1-base index の無向グラフ G
# 自己ループや多重辺も可

from sys import setrecursionlimit
setrecursionlimit(10**7)

visit = [0]*(N+1)
ord = [0]*(N+1)
low = [0]*(N+1)
bridge = []
def dfs(u, par=-1):
	ord[u] = ord[0]
	ord[0] += 1
	low[u] = ord[u]
	skipped = 0
	for v in G[u]:
		if not visit[v]:
			visit[v] = 1
			dfs(v, u)
			low[u] = min(low[u], low[v])
			if ord[u] < low[v]:
				bridge.append((u,v))
		elif par != v or skipped:
			low[u] = min(low[u], ord[v])
		else:
			# par==v and skipped==0
			skipped = 1
		continue
	return