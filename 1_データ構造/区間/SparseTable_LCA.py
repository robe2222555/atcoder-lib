# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/区間/SparseTable_LCA.py
def bl(a):
	res = 0
	while a>0:
		res += 1
		a >>= 1

	return res

class SparseTable:
	n: int
	h: int
	data: list[int]

	def __init__(self, seq, op=min):
		self.n = len(seq)
		self.op = op
		self.h = self.n.bit_length()
		#self.h = bl(self.n)
		self.data = [0]*(self.n*self.h)
		for i in range(self.n):
			self.data[i] = seq[i]
		for i in range(1,self.h):
			for j in range(self.n - (1<<i) + 1):
				self.data[i*self.n + j] = self.op(self.data[(i-1)*self.n + j], self.data[(i-1)*self.n + j+(1<<(i-1))])
	
	def prod(self, l ,r):
		# [l, r)
		level = (r - l).bit_length() - 1
		#level = bl((r - l)) - 1
		return self.op(self.data[level*self.n + l], self.data[level*self.n + r-(1<<level)])

class LCA:
	# sparse table 実装
	n: int
	G: list[list[int]]
	Depth: list[int]
	IN: list[int]
	root: int
	ST: SparseTable

	def __init__(self, N, r=1):
		self.n = N
		self.G = [[] for _ in range(N+1)]
		self.root = r

	def add_edge(self, u,v):
		self.G[u].append(v)

	def build(self):
		
		self.IN = [-1]*(self.n+1)
		self.Depth = [0]*(self.n+1)

		stk = [~self.root, self.root]
		visit = [0]*(self.n+1)
		visit[self.root] = 1
		time = 0
		dep = -1
		seq = []
		while stk:
			u = stk.pop()
			if u<0:
				dep -= 1
				seq.append(dep)
			else:
				dep += 1
				seq.append(dep)
				self.Depth[u] = dep

				self.IN[u] = time
				for v in self.G[u]:
					if visit[v]: continue
					visit[v] = 1
					stk.append(~v)
					stk.append(v)

			time += 1
			continue

		self.ST = SparseTable(seq)

	def dist(self, u,v):
		if u==v: return 0
		if self.IN[u] > self.IN[v]: u,v = v,u
		return self.Depth[u]+self.Depth[v]-2*self.ST.prod(self.IN[u], self.IN[v]+1)

