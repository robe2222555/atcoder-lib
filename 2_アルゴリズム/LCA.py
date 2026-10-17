# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/LCA.py
# 参考: https://algo-logic.info/lca/

class LowestCommonAncestor:
	"""
	最近共通祖先のダブリング実装
	"""
	G: list[list[int]]
	par: list[list[int]]
	depth: list[int]

	def __init__(self, N) -> None:
		self.msb=0
		self.N=N
		while (1<<self.msb)<N: self.msb+=1
		
		self.G = [[] for _ in range(N+1)]
		self.par=[[-1]*(N+1) for _ in range(self.msb+1)]

	def add_edge(self, u, v):
		self.G[u].append(v)
		self.G[v].append(u)
	
	def build(self, root):
		"""
		O(N \log N)
		"""
		self.root=root
		q=[root]
		self.Depth=[-1]*(self.N+1)
		self.Depth[root]=0
		while q:
			u = q.pop()
			for v in self.G[u]:
				if self.Depth[v]<0:
					self.Depth[v]=self.Depth[u]+1
					self.par[0][v]=u
					q.append(v)

		for k in range(self.msb):
			for v in range(1, self.N+1):
				self.par[k+1][v] = self.par[k][self.par[k][v]]

	def lca(self, a, b):
		"""
		a,b の最近共通祖先
		O(\log N)
		"""
		if a==b:
			return a
		if self.Depth[a] > self.Depth[b]:
			a,b = b,a

		# b を a と同じ深さまで上げる
		K = self.Depth[b]-self.Depth[a]
		for i in range(self.msb+1):
			if (K>>i)&1==1:
				b=self.par[i][b]
		if a==b:
			return a
		

		# par[0][a] = par[0][b] になるまでさかのぼる
		for i in range(self.msb,-1,-1):
			if self.par[i][a] != self.par[i][b]:
				a = self.par[i][a]
				b = self.par[i][b]
		assert self.par[0][a] == self.par[0][b]

		return self.par[0][a]

	def dist(self, a,b):
		"""
		頂点a~bの距離 = root~aの距離 - root~bの距離 - root~lca(a,b)の距離*2
		"""
		lca=self.lca(a,b)
		return self.Depth[a] + self.Depth[b] - 2*self.Depth[lca]
	
	def is_onpath(self, u, v, x):
		" return x \in (u, ..., v) "
		return self.dist(u, v) == self.dist(u, x) + self.dist(v, x)
