# https://github.com/robe2222555/atcoder-lib/blob/main/codon/LazySegTree.py
"""
codon 用の遅延セグ木

- verified by ABC322F
"""



INF = 1<<60
class LazySegTree:
	node: int
	dat: list[tuple[int, int, int, int, int, int, int]]
	lazy: list[int]

	dat_unit = (0,0, -1,-1, 0,0, 1)
	lazy_unit = 0

	def __init__(self, N):
		"""
		N	 : 元データ数
		dat  : セグ木の配列
		lazy : 遅延評価用の配列
		"""
		self.node=1
		while N>self.node: self.node*=2  #　木の最下層の葉の数

		self.dat = [self.dat_unit] * (self.node*2)
		self.lazy = [self.lazy_unit] * (self.node*2)
		return None
	
	# 要素モノイドの二項演算 x*y
	def op_dat(self, x, y):
		return (
			max(x[0], y[0], x[5]+y[4] if x[3]==y[2]==0 else 0), # 0の最大長
			max(x[1], y[1], x[5]+y[4] if x[3]==y[2]==1 else 0), # 1の最大長
			x[2] if x[2]>=0 else y[2], 		# 左端の値
			y[3] if y[3]>=0 else x[3], 		# 右端の値
			max(x[4], x[4]+y[4] if x[6] and x[3]==y[2] else 0), # 左端の値の最大長
			max(y[5], x[5]+y[5] if y[6] and x[3]==y[2] else 0), # 右端の値の最大長
			int(x[6]&y[6] and x[3]==y[2]) 	# すべて同じ文字か否か
		)

	# 作用素モノイドの二項演算 a*b
	def op_lazy(self, a, b):
		return a^b

	# 射影: dat x lazy -> dat
	def mapping(self, x, a):
		if a:
			return (
				x[1],
				x[0],
				x[2]^1,
				x[3]^1,
				x[4],
				x[5],
				x[6]
			)
		else:
			return x

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
		H = 0
		while (1<<H) <= i:
			H += 1
		H -= 1
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


	def bisearch(self, k=1):
		# 値0以下 かつ 個数1以上 の葉をすべて探索して，リセット
		# それら負の値の sum を返す

		# 節点 k の遅延評価を反映
		if self.node > k:
			self._propagate_at(k)
		else:
			self.dat[k] = self._eval_at(k)
			self.lazy[k] = self.lazy_unit


		MIN, SUM, _ = self.dat[k]
		if MIN>0:
			return 0

		if self.node > k:
			vl = self.bisearch(2*k)
			vr = self.bisearch(2*k+1)
			return vl+vr
		else:
			self.dat[k] = self.dat_unit
			self.lazy[k] = self.lazy_unit
			self._recalc_above(k)
			return MIN