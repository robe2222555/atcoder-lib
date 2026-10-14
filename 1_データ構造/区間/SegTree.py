
# 参考: https://maspypy.com/segment-tree-%E3%81%AE%E3%81%8A%E5%8B%89%E5%BC%B71
# 

class SegmentTree:
	def __init__(self, N, op, e):
		"""
		N : 数列のサイズ
		op: 二項演算
		e: 単位元
		dat : セグ木の配列, [1, N)=集約値 , [N, 2N)=数列の値
		
		pypy, codon 使用可
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