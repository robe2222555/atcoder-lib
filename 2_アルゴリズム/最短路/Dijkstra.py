# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/最短路/Dijkstra.py
# 基本形 + 経路復元

import heapq

INF = 1<<60
class Dijkstra:
	def __init__(self, N):
		self.n = N
		self.G = [[] for _ in range(N+1)]

	def add_edge(self, u, v, d):
		self.G[u].append((v, d))

	def search(self, s):
		"""
		:param s = 始点
		:return 始点から各点までの最短経路
		経路復元用の prev (最短路の直前の頂点) は self.prev に入る
		"""
		d = [INF]*(self.n + 1)
		self.s = s
		self.prev = [-1]*(self.n + 1)
		d[s] = 0
		q = []
		heapq.heappush(q, (0, s))
		visit = [0]*(self.n+1)
		while len(q):
			dis, u = heapq.heappop(q)
			if visit[u]:
				continue
			visit[u] = 1

			for v, cost in self.G[u]:
				if visit[v]: continue
				dis_p = dis+cost
				if d[v] > dis_p:
					d[v] = dis_p
					self.prev[v] = u
					heapq.heappush(q, (dis_p, v))

		return d

	def get_path(self, t):
		"""
		直前の search(s) について，頂点 s~t の最短経路を頂点の列で返す O(V)
		到達できない場合は []
		"""
		if t != self.s and self.prev[t] == -1:
			return []
		path = []
		while t != -1:
			path.append(t)
			t = self.prev[t]
		path.reverse()
		return path
