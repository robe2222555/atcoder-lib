# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/Tree/AuxiliaryTree.py
# 参考: https://atcoder.jp/contests/abc359/editorial/10259

class SparseTable:
	n: int
	h: int
	lg: list[int]
	data: list[int]

	def __init__(self, seq, op=min):
		self.n = len(seq)
		self.op = op
		self.lg = [0]*(self.n+1)
		for i in range(2, self.n+1):
			self.lg[i] = self.lg[i >> 1] + 1
		self.h = self.lg[self.n] + 1

		self.data = [0]*(self.n*self.h)
		for i in range(self.n):
			self.data[i] = seq[i]
		for i in range(1,self.h):
			for j in range(self.n - (1<<i) + 1):
				self.data[i*self.n + j] = self.op(self.data[(i-1)*self.n + j], self.data[(i-1)*self.n + j+(1<<(i-1))])
	
	def prod(self, l ,r):
		# [l, r)
		level = self.lg[r - l]
		return self.op(self.data[level*self.n + l], self.data[level*self.n + r-(1<<level)])


class LowestCommonAncestor:
	# sparse table 実装
	n: int
	G: list[list[int]]
	Depth: list[int]
	preorder: list[int]
	root: int
	ST: SparseTable

	def __init__(self, N, r=1):
		self.n = N
		self.G = [[] for _ in range(N+1)]
		self.root = r

	def argmin(self, u, v):
		return u if self.Depth[u] <= self.Depth[v] else v

	def add_edge(self, u,v):
		self.G[u].append(v)

	def build(self):
		self.preorder = [-1]*(self.n+1)
		self.Depth = [0]*(self.n+1)

		stk = [~self.root, self.root]
		visit = [0]*(self.n+1)
		visit[self.root] = 1
		time = 0
		dep = -1
		tour = []

		while stk:	# traverseを取るタイプのdfs
			u = stk.pop()
			if u<0:
				dep -= 1
				tour.append(~u)
			else:
				dep += 1
				tour.append(u)
				self.Depth[u] = dep

				self.preorder[u] = time
				for v in self.G[u]:
					if visit[v]: continue
					visit[v] = 1
					stk.append(~u)	# 親
					stk.append(v)

			time += 1
			continue

		self.ST = SparseTable(tour, op=self.argmin)

	def lca(self, u, v):
		if self.preorder[u] > self.preorder[v]: u,v = v,u
		return self.ST.prod(self.preorder[u], self.preorder[v]+1)

	def dist(self, u,v):
		if u==v: return 0
		return self.Depth[u]+self.Depth[v]-2*self.Depth[self.lca(u, v)]


class AuxiliaryTree(LowestCommonAncestor):
	AT: list[list[int]]		# 構築結果

	def build(self):
		super().build()
		self.AT = [[] for _ in range(self.n+1)]

	def query(self, vs: list[int]):
		"""
		vs: ターミナルとなる頂点集合
		return: 根となる頂点
		"""
		vs.sort(key=lambda u:self.preorder[u])
		k = len(vs)

		stk = [vs[0]]
		self.AT[vs[0]].clear()
		for i in range(k-1):
			p = self.lca(vs[i], vs[i+1])
			if p != vs[i]:
				last = stk.pop()
				while stk and self.Depth[p] < self.Depth[stk[-1]]:
					self.AT[stk[-1]].append(last)
					last = stk.pop()

				if not stk or stk[-1] != p:
					stk.append(p)
					#vs.append(p)	# 追加される頂点
					self.AT[p] = [last]
				else:
					self.AT[p].append(last)

			stk.append(vs[i+1])
			self.AT[vs[i+1]].clear()

		for i in range(len(stk)-1):
			self.AT[stk[i]].append(stk[i+1])
		return stk[0]