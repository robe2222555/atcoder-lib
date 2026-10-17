# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/SCC/SCC_nonrec.py
# 参考: 非再帰dfs https://qiita.com/Kiri8128/items/2b0023bed9af642c751c
# verified by https://www.share-oj.net/problems/03ab3a91-31a5-43f0-b3fb-bd5329ed7d66
#  "非"再帰実装

# scc_i := トポソしたDAG上で，i番目の強連結成分の頂点集合
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