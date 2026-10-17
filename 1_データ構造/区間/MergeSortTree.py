# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/区間/MergeSortTree.py
# verified by ABC339G
# 以下の実装は x 以下の総和を求めるver

from bisect import bisect_left, bisect_right
def merge(A,B):
	pos = 0
	res = [0]*(len(A)+len(B))
	for i in range(len(A)):
		a = A[i]
		while pos<len(B) and B[pos] < a:
			res[i+pos] = B[pos]
			pos += 1
		
		res[i+pos] = a

	while pos<len(B):
		res[len(A)+pos] = B[pos]
		pos += 1

	return res


INF = 1<<60
class MergeSortTree:
	def __init__(self, N): # N:要素数
		"""
		N : 元データ数
		dat : セグ木の配列, [1, N)=集約値 , [N, 2N)=数列の値
		"""
		self._N = N
		self.node=1
		while N>self.node: self.node*=2  #　木の最下層の葉の数
		self.dat  = [[INF] for _ in range(self.node*2)] # 1-indexed
		self.acc  = [[INF] for _ in range(self.node*2)] # 1-indexed
		return

	def value_i(self, i):
		return self.dat[i+self.node]
	

	def build(self, seq):
		for i, x in enumerate(seq, self.node):
			self.dat[i] = [x]
			self.acc[i] = [x]
		for i in range(self.node - 1, 0, -1):
			self.dat[i] = merge(self.dat[2*i], self.dat[2*i+1])
			self.acc[i] = [x for x in self.dat[i]]
			for j in range(1, len(self.acc[i])):
				self.acc[i][j] += self.acc[i][j-1]
		
		return None

	
	def sum_filter(self, i, x):
		pos = bisect_right(self.dat[i], x)-1
		if pos < 0:
			return 0, 0
		else:
			return self.acc[i][pos], len(self.dat[i])-pos-1



	def query(self, a, b, x):
		"""
		区間 A[a, b) のうち x 以下のものの総和と個数を求める
		a,b は 0-based index
		"""

		L = a+self.node
		R = b+self.node
		SUM, CNT = 0,0
		# bottom-up
		while L < R:
			if L & 1:
				s,c = self.sum_filter(L, x)
				SUM += s
				CNT += c
				L += 1
			if R & 1:
				R -= 1
				s,c = self.sum_filter(R, x)
				SUM += s
				CNT += c
			L >>= 1
			R >>= 1
		return SUM, CNT
	

	def KthSmallestElement(self, a, b, k):
		"""
		区間 A[a, b) のうち，k 番目に小さい要素を返す
		注意: まだ verify していない
		"""
		assert 0 < k <= b-a
		ok = self.dat[self.node][0]
		ng = self.dat[self.node+self._N-1][0] + 1

		while ng-ok>1:
			mid = (ok+ng)//2
			_,c = self.query(a, b, mid)
			if c <= mid:
				ok = mid
			else:
				ng = mid
			continue
		return ok
