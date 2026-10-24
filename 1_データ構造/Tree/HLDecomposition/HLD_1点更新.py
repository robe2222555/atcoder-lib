# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/Tree/HLDecomposition/HLD_1点更新.py
# 参考: https://info.atcoder.jp/entry/algorithm_lectures/heavy_light_decomposition

from sys import setrecursionlimit
setrecursionlimit(10**7)
mod = 998244353

class SegmentTree:
	def __init__(self, N, op, e):
		"""
		N : 数列のサイズ
		op: 二項演算
		e: 単位元
		dat : セグ木の配列, [1, N)=集約値 , [N, 2N)=数列の値
		"""
		self.node=1
		while N>self.node: self.node*=2  #　木の最下層の葉の数
		self.operate = op
		self.dat_unit = e
		
		self.dat  = [self.dat_unit]*(self.node*2) # 1-indexed
		return

	def value_i(self, i):
		return self.dat[i+self.node]

	def build(self, seq):
		for i, x in enumerate(seq, self.node):
			self.dat[i] = x
		for i in range(self.node - 1, 0, -1):
			self.dat[i] = self.operate(self.dat[2*i], self.dat[2*i+1])
		return None

	
	def query(self, a, b):
		"""
		区間[a, b) のdatの集約値を返す
		a,b は 0-based index
		"""

		L = a+self.node
		R = b+self.node
		vL = self.dat_unit
		vR = self.dat_unit
		# bottom-up
		while L < R:
			if L & 1:   
				vL = self.operate(vL, self.dat[L])
				L += 1
			if R & 1:
				R -= 1
				vR = self.operate(self.dat[R], vR)
			L >>= 1
			R >>= 1
		return self.operate(vL, vR)


	def add(self, a, val, replace=False):
		"""
		dat[a]にvalを作用
		a は 0-based index
		replace=Trueで値を書き換える
		"""
		a += self.node

		if replace:
			self.dat[a] = val
		else:
			self.dat[a] = self.operate(self.dat[a], val)
	
		while a>1:
			a = a >> 1
			self.dat[a] = self.operate(self.dat[2*a], self.dat[2*a+1])

		return None

	def upper_bound(self, L, func):
		"""
		入力 index L, 条件 func
		出力 R := func(dat[L, R)の集約値)=True を満たす最大のindex
		"""
		if L >= self.node:
			return self.node

		L += self.node
		sm = self.dat_unit
		first = True
		while first or (L & -L) != L:
			first = False
			while L%2==0: L >>= 1

			if not func(self.operate(sm, self.dat[L])):
				while L < self.node:
					L <<= 1
					if func(self.operate(sm, self.dat[L])):
						sm = self.operate(sm, self.dat[L])
						L += 1
				return L - self.node
			else:
				sm = self.operate(sm, self.dat[L])
				L += 1

		return self.node	# 未発見

	def lower_bound(self, R, func):
		"""
		入力 index R, 条件 func
		出力 L := func(dat[L, R)の集約値)=True を満たす最小のindex
		"""
		if R <= 0:
			return 0

		R += self.node
		sm = self.dat_unit
		first = True
		while first or (R & -R) != R:
			first = False
			R -= 1
			while R > 1 and R % 2 == 1: R >>= 1

			if not func(self.operate(self.dat[R], sm)):
				while R < self.node:
					R = 2 * R + 1
					if func(self.operate(self.dat[R], sm)):
						sm = self.operate(self.dat[R], sm)
						R -= 1
				return R + 1 - self.node
			sm = self.operate(self.dat[R], sm)

		return 0
	
	def __repr__(self):
		return "Seg: " + str(self.dat[self.node:])


def _identity(x): return x

class HLDecomposition:
	def __init__(self, N, op, e, rev=_identity) -> None:
		"""
		op: モノイドの二項演算
		e: モノイドの単位元
		rev: モノイドの順方向と逆方向を反転させる演算 (可換なら省略可)
		pypy,codonで可能
		"""
		self.N=N
		self.G: list[list[int]] = [[] for _ in range(N+1)]
		self.rev = rev
		self.is_edge = False
		self.root = -1
		self.par = [-1]*(N+1)
		self.pre = [-1]*(N+1)	# heavy child 優先 dfs の pre-order
		self.tour: list[int] = []	# pre の頂点列
		self.head = list(range(N+1))	# v を通る heavy path の先頭 (根側)
		self.Seg = SegmentTree(N, op, e)

	def add_edge(self, u, v):
		self.G[u].append(v)

	def build(self, root, W=None, E=None, is_edge=False):
		"""
		W: 頂点重み (長さ N+1 の配列)
		E: 辺重み [(u, v, w), ...]
		is_edge: True で辺重み (辺の値は子側の頂点に持たせる)
		"""
		self.is_edge = is_edge
		self.root=root
		hc = [-1]*(self.N+1)	# 親 u から見たときの heavy child

		def dfs1(u, p=-1):	# heavy child を求める
			szu = 1
			szhc = 0
			for v in self.G[u]:
				if v==p: continue
				self.par[v] = u
				tmp = dfs1(v, u)
				szu += tmp
				if szhc < tmp:	# heavy child
					szhc = tmp
					hc[u] = v
			return szu

		def dfs2(u, p=-1):
			self.pre[u] = len(self.tour)
			self.tour.append(u)
			v = hc[u]

			if v<0: return
			self.head[v] = self.head[u]
			dfs2(v, u)	# heavy child 優先

			for v in self.G[u]:	# light child
				if v==p: continue
				if v==hc[u]: continue
				dfs2(v, u)
			return

		dfs1(root)
		dfs2(root)

		if not W is None:
			self.Seg.build([W[u] for u in self.tour])
		if not E is None:	# 辺重みを子側の頂点重みに変換
			A = [self.Seg.dat_unit]*(self.N+1)
			for u, v, w in E:
				A[self.edge_vertex(u, v)] = w
			self.Seg.build([A[u] for u in self.tour])
		return

	def is_same_hpath(self, u, v):
		return self.head[u] == self.head[v]

	def culc_order_hpath(self, u):
		return self.pre[u] - self.pre[self.head[u]]

	def edge_vertex(self, u, v):
		"""
		辺 u-v の値を持つ頂点 (子側)
		"""
		return v if self.par[v] == u else u

	def add_v(self, u, x, is_replace=False):
		self.Seg.add(self.pre[u], x, is_replace)

	def add_e(self, u, v, x, is_replace=False):
		self.Seg.add(self.pre[self.edge_vertex(u, v)], x, is_replace)

	def lca(self, u, v):
		if u==v: return u

		while self.head[u] != self.head[v]:
			if self.pre[u] > self.pre[v]:
				u = self.par[self.head[u]]
			else:
				v = self.par[self.head[v]]
			continue

		if self.pre[u] < self.pre[v]:
			return u
		else:
			return v


	def fold(self, u, v):
		"""
		path u-v のクエリ
		"""
		LCA = self.lca(u, v)
		U = self.Seg.dat_unit
		V = self.Seg.dat_unit
		op = self.Seg.operate

		# U := (lca, u]
		while self.head[u] != self.head[LCA]:
			h = self.head[u]
			# 葉から遡ってるので逆, (nx, u]
			U = op(self.Seg.query(self.pre[h], self.pre[u]+1), U)
			u = self.par[h]
			continue
		U = op(self.Seg.query(self.pre[LCA]+1, self.pre[u]+1), U)

		# V := (lca, v]
		while self.head[v] != self.head[LCA]:
			h = self.head[v]
			# 葉から遡ってるので逆, (nx, u]
			V = op(self.Seg.query(self.pre[h], self.pre[v]+1), V)
			v = self.par[h]
			continue
		V = op(self.Seg.query(self.pre[LCA]+1, self.pre[v]+1), V)

		# U,LCA,Vをマージ (辺重みなら LCA は含めない)
		if not self.is_edge:
			U = op(self.Seg.value_i(self.pre[LCA]), U)
		return op(self.rev(U), V)