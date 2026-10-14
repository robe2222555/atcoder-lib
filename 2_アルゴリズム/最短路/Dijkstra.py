
################
# 基本形

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
		"""
		d = [INF]*(self.n + 1)
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
					heapq.heappush(q, (dis_p, v))

		return d





###############################



# ダイクストラ fromあり本
# O(ElogV)

import heapq as hq
import collections

INF=float("inf")
V, E=LI()
# 始点，終点，コスト
Edge=[LI() for _ in range(E)]
G=[[] for _ in range(V)]
for s,t,cost in Edge:
	G[s].append([t, cost])
	G[t].append([s, cost])

# 最短路の直前の頂点
prev=[-1]*V

import heapq as hq
import collections

def dijkstra(s):
	d = collections.defaultdict(lambda: float('inf'))
	d[s] = 0
	q = []
	hq.heappush(q, (0, s))
	visit = collections.defaultdict(bool)
	while len(q):
		st_dis, st = hq.heappop(q)
		if visit[st]:
			continue
		visit[st] = True

		for to, cost in G[st]:
			if visit[to]:
				continue
			if d[to] > st_dis+cost:
				d[to]=st_dis+cost
				prev[to]=st
				hq.heappush(q, (d[to], to))
	return d

# 頂点s~tへの最短経路 O(V)
def get_path(t):
	path=[]
	while t!=-1:
		path.append(t)
		t=prev[t]
	path.reverse()
	return path

dijkstra(0)
print(get_path(6))
##################################

# あり本 p102 二番目の最短路計算 O(ElogV)
# 前処理は同じ

prev=[-1]*V
def dijkstra(s):
	d1 = collections.defaultdict(lambda: float('inf'))
	d2 = collections.defaultdict(lambda: float('inf'))
	d1[s] = 0
	q = []
	hq.heappush(q, (0, s))
	while len(q):
		st_dist, st = hq.heappop(q)
		if st_dist>d2[st]: # 2番目の最短路まで確定したらcontinue
			continue

		for to, cost in G[st]:
			to_dist=st_dist+cost
			# 1番目の最短路の候補をheapに入れる
			if d1[to] > to_dist:
				d1[to]=to_dist
				prev[to]=st
				hq.heappush(q, (d1[to], to))
			
			# 2番目の最短路の候補をheapに入れる
			if d2[to]>to_dist>d1[to]:
				d2[to]=to_dist
				hq.heappush(q, (d2[to], to))
	return d1, d2

##################################




##################################
import collections
import heapq


class Dijkstra:
	def __init__(self):
		self.e = collections.defaultdict(list)

	def add(self, u, v, d):
		self.e[u].append([v, d])
		self.e[v].append([u, d])

	def delete(self, u, v):
		self.e[u] = [_ for _ in self.e[u] if _[0] != v]
		self.e[v] = [_ for _ in self.e[v] if _[0] != u]

	def search(self, s):
		"""
		:param s: 始点
		:return: 始点から各点までの最短経路
		"""
		d = collections.defaultdict(lambda: float('inf'))
		d[s] = 0
		q = []
		heapq.heappush(q, (0, s))
		v = collections.defaultdict(bool)
		while len(q):
			k, u = heapq.heappop(q)
			if v[u]:
				continue
			v[u] = True

			for uv, ud in self.e[u]:
				if v[uv]:
					continue
				vd = k + ud
				if d[uv] > vd:
					d[uv] = vd
					heapq.heappush(q, (vd, uv))

		return d


##############################

import collections
import heapq


class Dijkstra():
	def __init__(self):
		self.e = collections.defaultdict(list)

	def add(self, u, v, d, directed=False):
		"""
		#0-indexedでなくてもよいことに注意
		#u = from, v = to, d = cost
		#directed = Trueなら、有向グラフである
		"""
		if directed is False:
			self.e[u].append([v, d])
			self.e[v].append([u, d])
		else:
			self.e[u].append([v, d])

	def delete(self, u, v):
		self.e[u] = [_ for _ in self.e[u] if _[0] != v]
		self.e[v] = [_ for _ in self.e[v] if _[0] != u]

	def Dijkstra_search(self, s):
		"""
		#0-indexedでなくてもよいことに注意
		#:param s: 始点
		#:return: 始点から各点までの最短経路と最短経路を求めるのに必要なprev
		"""
		d = collections.defaultdict(lambda: float('inf'))
		prev = collections.defaultdict(lambda: None)
		d[s] = 0
		q = []
		heapq.heappush(q, (0, s))
		v = collections.defaultdict(bool)
		while len(q):
			k, u = heapq.heappop(q)
			if v[u]:
				continue
			v[u] = True

			for uv, ud in self.e[u]:
				if v[uv]:
					continue
				vd = k + ud
				if d[uv] > vd:
					d[uv] = vd
					prev[uv] = u
					heapq.heappush(q, (vd, uv))

		return d, prev

	def getDijkstraShortestPath(self, start, goal):
		_, prev = self.Dijkstra_search(start)
		shortestPath = []
		node = goal
		while node is not None:
			shortestPath.append(node)
			node = prev[node]
		return shortestPath[::-1]