# ======================
#  "非"再帰実装
# verified by https://www.share-oj.net/problems/03ab3a91-31a5-43f0-b3fb-bd5329ed7d66
# scc[i] は トポソしたDAGの頂点番号に対応
# ======================


# scc_i := i番目の強連結成分の頂点集合
def SCC_nonrec(G, N):
	G_reverse = [[] for _ in range(N+1)]
	for u in range(N+1):
		for v in G[u]:
			G_reverse[v].append(u)

	visit = [0]*(N+1)
	def culc_postorder(st, _G):
		"""
		_G の dfs木のpost-orderを求める
		"""
		stk = [st]
		res = []
		while stk:
			u = stk.pop()
			if u >= 0:
				if visit[u]: continue
				visit[u] = 1
				stk.append(~u)
				for v in _G[u]:
					if visit[v]: continue
					stk.append(v)
			else:
				res.append(~u)
		return res
	
	# dfs 1回目
	post = []
	for st in range(1, N+1):
		if visit[st]: continue
		post += culc_postorder(st, G)


	# dfs 2回目
	scc=[]
	for i in range(N+1): visit[i] = 0
	for st in post[::-1]:
		if visit[st]: continue
		scc.append(culc_postorder(st, G_reverse))

	return scc, post


##########################################

# 再帰実装
from sys import setrecursionlimit
setrecursionlimit(10**8)

# scc_i := i番目の強連結成分の頂点集合
def SCC(G, N) -> list[list[int]]:
	G_reverse = [[] for _ in range(N+1)]
	for u in range(N+1):
		for v in G[u]:
			G_reverse[v].append(u)

	visit = [0]*(N+1)
	post = []
	def dfs(u):
		for v in G[u]:
			if visit[v]: continue
			visit[v] = 1
			dfs(v)
		post.append(u)
		return
	for u in range(1, N+1):
		if visit[u]: continue
		visit[u] = 1
		dfs(u)

	scc = []
	for i in range(1, N+1): visit[i] = 0
	def dfs_rev(u):
		scc[-1].append(u)
		for v in G_reverse[u]:
			if visit[v]: continue
			visit[v] = 1
			dfs_rev(v)
		
		return

	for u in post[::-1]:
		if visit[u]: continue
		visit[u] = 1
		scc.append([])
		dfs_rev(u)
	return scc