# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/UnionFind.py

class UnionFind():
	def __init__(self, n):
		"0-base index"
		self.n = n
		self.par = list(range(n))
		self.rank = [0]*n
		self.group_num = n
		self.sz = [1]*n

	def find(self, x):
		"ノードxが属する集合の根を求める"
		if self.par[x] == x:
			return x
		else:
			self.par[x] = self.find(self.par[x])
			return self.par[x]

	def unite(self, x, y):
		"xとyの属する集合を併合"
		x = self.find(x)
		y = self.find(y)

		if x == y:
			return
		
		if self.rank[x] < self.rank[y]:
			self.par[x] = y
			self.sz[y] += self.sz[x]
		else:
			self.par[y] = x
			self.sz[x] += self.sz[y]
			if self.rank[x] == self.rank[y]:
				self.rank[x] += 1
		self.group_num-=1

	def same(self, x, y):
		"xとyが同じ集合に属するか否か"
		return self.find(x) == self.find(y)
	
	def size(self, x):
		"頂点 x と同じ連結成分の頂点の個数"
		return self.sz[self.find(x)]


	def groups(self, is_1_indexed = True) -> list:
		root_buf = [self.find(i) for i in range(self.n)]

		res = [[] for _ in range(self.n)]
		for i in range(int(is_1_indexed), self.n):
			res[root_buf[i]].append(i)

		return list(filter(lambda r: r, res))

