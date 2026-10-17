# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/全域木/prim法.py
# 参考: あり本

"""
プリム法
重み付き無向グラフ (全部連結している) の最小全域木をつくる　辺のコスト和が最小の木
一つの頂点 s からなる木 T を考える
ほかの頂点から T に接続している辺のうち,最小のものを T に付け加える
最小のものは heap でとる
O(E*logV)

頂点番号は 1-indexed (1 ~ N)
"""

import heapq

class Prim:
	def __init__(self, N):
		self.n = N
		self.G = [[] for _ in range(N+1)]

	def add_edge(self, u, v, cost):
		self.G[u].append((v, cost))

	def search(self, s):
		"""
		:param s = 始点
		:return (最小全域木のコスト和, 確定した頂点 visit, 追加した頂点数 cnt (始点を除く))
		連結なら cnt = N-1
		"""
		res = 0
		q = []
		visit = [0]*(self.n+1)
		visit[s] = 1
		cnt = 0
		for v, cost in self.G[s]:
			heapq.heappush(q, (cost, v))

		while q and cnt < self.n:
			cost, u = heapq.heappop(q)
			if visit[u]: continue
			visit[u] = 1
			cnt += 1
			res += cost

			for v, cost in self.G[u]:
				if visit[v]: continue
				heapq.heappush(q, (cost, v))

		return res, visit, cnt
