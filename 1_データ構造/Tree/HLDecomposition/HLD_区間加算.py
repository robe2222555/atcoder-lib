# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/Tree/HLDecomposition/HLD_区間加算.py
# 参考: https://info.atcoder.jp/entry/algorithm_lectures/heavy_light_decomposition
# verified by https://atcoder.jp/contests/awc0183/tasks/awc0183_e

from sys import setrecursionlimit
setrecursionlimit(10**7)
mod = 998244353

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

class LazySegTree:
	def __init__(self, N, op1, uni1, op2, uni2, op3):
		"""
		N		: 元データ数
		op1 	: 要素モノイドの二項演算
		uni1	: 要素モノイドの単位元
		op2		: 作用素モノイドの二項演算
		uni2	: 作用素モノイドの単位元
		op3		: 射影: dat x lazy -> dat

		pypy, codon 使用可
		"""
		self.node=1
		while N>self.node: self.node*=2  #　木の最下層の葉の数
		self.op_dat = op1
		self.op_lazy = op2
		self.dat_unit = uni1
		self.lazy_unit = uni2
		self.mapping = op3

		self.dat = [self.dat_unit] * (self.node*2)
		self.lazy = [self.lazy_unit] * (self.node*2)
		return None

	def __repr__(self):
		return "LazySeg: " + str(self.dat[self.node:])

	def build(self, seq):
		for i, x in enumerate(seq, self.node):
			self.dat[i] = x
		for i in range(self.node - 1, 0, -1):
			self.dat[i] = self.op_dat(self.dat[i << 1], self.dat[i << 1 | 1])
		return None

	# 節点 i の遅延評価後の値を返す
	def _eval_at(self, i):
		return self.mapping(self.dat[i], self.lazy[i])
	
	# 節点 i の遅延評価を反映し，子に伝搬
	def _propagate_at(self, i):
		if i>=self.node:
			self.dat[i] = self._eval_at(i)
			self.lazy[i] = self.lazy_unit
			return None
		else:
			self.dat[i] = self._eval_at(i)
			self.lazy[i << 1] = self.op_lazy(self.lazy[i << 1], self.lazy[i])
			self.lazy[i << 1 | 1] = self.op_lazy(self.lazy[i << 1 | 1], self.lazy[i])
			self.lazy[i] = self.lazy_unit
			return None

	# 根 から i の遅延評価を反映/伝搬
	def _propagate_above(self, i):
		H = msb(i)
		for h in range(H, 0, -1):
			self._propagate_at(i >> h)
		return None

	# i から 根 へ要素モノイドの再計算をする
	def _recalc_above(self, i):
		# iより上はすべて評価済みが前提
		while i > 1:
			i >>= 1
			#assert(self.lazy[i] == self.lazy_unit)
			self.dat[i] = self.op_dat(self._eval_at(2*i), self._eval_at(i*2+1))
		return None

	def eval_all(self):
		for i in range(1, self.node*2):
			self._propagate_at(i)
		return None


	# x_iの値をxに置き換える iは0-based index
	# 上方から伝播 -> 値変更 -> 上方へ再計算
	def set_val(self, i, x):
		i += self.node
		self._propagate_above(i)
		self.dat[i] = x
		self.lazy[i] = self.lazy_unit
		self._recalc_above(i)

	# [L, R)のクエリ
	# 対象区間の端を基準に上方から伝播 -> 下から対象区間を探索して集計していく
	def fold(self, L, R):
		L += self.node
		R += self.node
		self._propagate_above(L // (L & -L))
		self._propagate_above(R // (R & -R) - 1)
		vL = self.dat_unit
		vR = self.dat_unit
		while L < R:
			if L & 1:
				vL = self.op_dat(vL, self._eval_at(L))
				L += 1
			if R & 1:
				R -= 1
				vR = self.op_dat(self._eval_at(R), vR)
			L >>= 1
			R >>= 1
		return self.op_dat(vL, vR)

	# [L, R)の対象区間に作用xを加える
	def apply(self, L, R, x):
		L += self.node
		R += self.node
		L0 = L // (L & -L)      # Lの真上にあり かつ 左の子である 最も高い位置にあるノード
		R0 = R // (R & -R) - 1  # R-1の真上にあり かつ 右の子である 最も高い位置にあるノード
		self._propagate_above(L0)
		self._propagate_above(R0)
		while L < R:
			if L & 1:
				self.lazy[L] = self.op_lazy(self.lazy[L], x)
				L += 1
			if R & 1:
				R -= 1
				self.lazy[R] = self.op_lazy(self.lazy[R], x)
			L >>= 1
			R >>= 1
		self._recalc_above(L0)
		self._recalc_above(R0)



	# 在庫が0以下のものを葉までさかのぼり，それをリセット後に上へ再計算
	# 返り値は0以下の在庫数の総和
	def bisearch(self, k=1):
		# 節点 k の遅延評価を反映
		if self.node > k:
			self._propagate_at(k)
		else:
			self.dat[k] = self._eval_at(k)
			self.lazy[k] = self.lazy_unit

		_, MIN = self.dat[k]
		if MIN>0:
			return 0

		if self.node > k:
			vl = self.bisearch(2*k)
			vr = self.bisearch(2*k+1)
			return vl+vr
		else:
			self.lazy[k] = self.lazy_unit
			self.dat[k] = self.dat_unit
			self._recalc_above(k)
			return -MIN

	def upper_bound(self, L, func):
		"""
		入力 index L, 条件 func
		出力 R := func(dat[L, R)の集約値)=True を満たす最大のindex
		"""
		if L >= self.node:
			return self.node

		L += self.node
		self._propagate_above(L)
		sm = self.dat_unit
		first = True
		while first or (L & -L) != L:
			first = False
			L = L // (L & -L)
			self._propagate_at(L)

			if not func(self.op_dat(sm, self.dat[L])):
				while L < self.node:
					L <<= 1
					self._propagate_at(L)
					if func(self.op_dat(sm, self.dat[L])):
						sm = self.op_dat(sm, self.dat[L])
						L += 1
				return L - self.node
			else:
				sm = self.op_dat(sm, self.dat[L])
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
		self._propagate_above(R)
		sm = self.dat_unit
		first = True
		while first or (R & -R) != R:
			first = False
			R -= 1
			R = R // (R & -R)

			if not func(self.op_dat(self.dat[R], sm)):
				while R < self.node:
					R = 2 * R + 1
					self._propagate_at(R)
					if func(self.op_dat(self.dat[R], sm)):
						sm = self.op_dat(self.dat[R], sm)
						R -= 1
						self._propagate_at(R)
				return R + 1 - self.node
			sm = self.op_dat(self.dat[R], sm)

		return 0

def _identity(x): return x

class HLDecomposition:
	def __init__(self, N, op1, e1, op2, e2, op3, rev=_identity) -> None:
		"""
		op1, e1: 要素モノイドの二項演算と単位元
		op2, e2: 作用素モノイドの二項演算と単位元
		op3: 作用素の要素に対する射影
		rev: モノイドの順方向と逆方向を反転させる演算 (可換なら省略可)

		pypy,codonで使用可
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
		self.Seg = LazySegTree(N, op1, e1, op2, e2, op3)

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

	def set_val(self, u, x):
		self.Seg.set_val(self.pre[u], x)

	def set_edge(self, u, v, x):
		self.Seg.set_val(self.pre[self.edge_vertex(u, v)], x)

	def apply(self, u, v, x):
		"""
		path u-v に x を作用
		"""
		LCA = self.lca(u, v)

		# (lca, u]
		while self.head[u] != self.head[LCA]:
			h = self.head[u]
			self.Seg.apply(self.pre[h], self.pre[u]+1, x)
			u = self.par[h]
			continue
		self.Seg.apply(self.pre[LCA]+1, self.pre[u]+1, x)

		# (lca, v]
		while self.head[v] != self.head[LCA]:
			h = self.head[v]
			self.Seg.apply(self.pre[h], self.pre[v]+1, x)
			v = self.par[h]
			continue
		self.Seg.apply(self.pre[LCA]+1, self.pre[v]+1, x)

		# lca (辺重みなら含めない)
		if not self.is_edge:
			self.Seg.apply(self.pre[LCA], self.pre[LCA]+1, x)

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
		op = self.Seg.op_dat

		# U := (lca, u]
		while self.head[u] != self.head[LCA]:
			h = self.head[u]
			# 葉から遡ってるので逆, (nx, u]
			U = op(self.Seg.fold(self.pre[h], self.pre[u]+1), U)
			u = self.par[h]
			continue
		U = op(self.Seg.fold(self.pre[LCA]+1, self.pre[u]+1), U)

		# V := (lca, v]
		while self.head[v] != self.head[LCA]:
			h = self.head[v]
			# 葉から遡ってるので逆, (nx, u]
			V = op(self.Seg.fold(self.pre[h], self.pre[v]+1), V)
			v = self.par[h]
			continue
		V = op(self.Seg.fold(self.pre[LCA]+1, self.pre[v]+1), V)

		# U,LCA,Vをマージ (辺重みなら LCA は含めない)
		if not self.is_edge:
			U = op(self.Seg.fold(self.pre[LCA], self.pre[LCA]+1), U)
		return op(self.rev(U), V)