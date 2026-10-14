# 参考: https://maspypy.com/segment-tree-%e3%81%ae%e3%81%8a%e5%8b%89%e5%bc%b72

class LazySegTree:
	def __init__(self, N, op1, uni1, op2, uni2, op3):
		"""
		N		: 元データ数
		op1 	: 要素モノイドの二項演算
		uni1	: 要素モノイドの単位元
		op2		: 作用素モノイドの二項演算
		uni2	: 作用素モノイドの単位元
		op3		: 射影: dat x lazy -> dat
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
		H = i.bit_length() - 1
		for h in range(H, 0, -1):
			self._propagate_at(i >> h)
		return None

	# i から 根 へ要素モノイドの再計算をする
	def _recalc_above(self, i):
		# iより上はすべて評価済みが前提
		while i > 1:
			i >>= 1
			assert(self.lazy[i] == self.lazy_unit)
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