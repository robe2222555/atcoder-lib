# 内部は 1-indexed実装だけど，インターフェイスは 0-base
# codon でも可能
class BIT:
	def __init__(self, n):
		self.n = n              # 要素数
		self.bit = [0]*(n+1)    # 木の値
		self.data = [0]*(n+1)   # 要素の値　格納先は1-indexed

	def build(self, seq):
		for i in range(1, len(seq)+1):
			self.data[i] = seq[i-1]
			self.bit[i] = seq[i-1]
		for i in range(1, self.n+1):
			j = i + (i & -i)
			if j <= self.n:
				self.bit[j] += self.bit[i]

	
	def sum(self, l, r):
		# A[l, r) の総和
		return self._sum(r) - self._sum(l)

	def _sum(self, i):
		# A[0, i) の総和
		res = 0
		while i > 0:
			res += self.bit[i]
			rsb = i & -i
			i -= rsb
		return res
	
	
	def add(self, i, x, replace=False):
		# A[i]+=x  or  A[i] \gets x
		i += 1
		if replace:
			x -= self.data[i]
		self.data[i] += x
		while i <= self.n:
			self.bit[i] += x
			rsb = i & -i
			i += rsb

	def lower_bound(self, w):
		# sum(A[0, r)) < w を満たす最大の r
		if w<=0:
			return 0
		x=0
		r=1
		while r<=self.n:
			r=r<<1

		sz=r   # 配列の長さ
		while sz>0:
			if (x+sz <= self.n) and self.bit[x+sz]<w: # 採用
				w-=self.bit[x+sz]
				x+=sz
			sz=sz>>1

		return x