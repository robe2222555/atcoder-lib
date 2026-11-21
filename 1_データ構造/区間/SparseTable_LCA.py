# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/区間/SparseTable_LCA.py

def msb(x: int) -> int:
	# 最上位ビットの位置（= bit_length - 1）
	r = 0
	if x >> 32: x >>= 32; r += 32
	if x >> 16: x >>= 16; r += 16
	if x >> 8:  x >>= 8;  r += 8
	if x >> 4:  x >>= 4;  r += 4
	if x >> 2:  x >>= 2;  r += 2
	if x >> 1:  r += 1
	return r


class SparseTable:
	n: int
	h: int
	data: list[int]

	def __init__(self, seq, op=min):
		self.n = len(seq)
		self.op = op
		self.h = msb(self.n)+1
		self.data = [0]*(self.n*self.h)
		for i in range(self.n):
			self.data[i] = seq[i]
		for i in range(1,self.h):
			for j in range(self.n - (1<<i) + 1):
				self.data[i*self.n + j] = self.op(self.data[(i-1)*self.n + j], self.data[(i-1)*self.n + j+(1<<(i-1))])
	
	def prod(self, l ,r):
		# [l, r)
		level = msb(r - l)
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
