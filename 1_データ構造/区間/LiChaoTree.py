# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/区間/LiChaoTree.py
# 非再帰実装
# オーバーフローに注意

class LiChaoTree:
	INF = 1<<60
	dat_unit = INF

	@classmethod
	def operate(cls, x, y):
		return min(x, y)
	
	def sign(self, x, y):
		return x>y	# max なら x<y
	
	def __init__(self, X):
		"""
		X : 点集合
		dat : セグ木の配列, [1, N)=集約値 , [N, 2N)=数列の値

		lmr[i]	:= 節点 i が支配する閉区間とその中間の点 (l, m, r)
		F[i]	:= i 番目の直線 (傾き, 切片)
		"""
		X = sorted(list(set(X)))
		self.node = 1<<(len(X)-1).bit_length()

		self.X = X + [self.INF]*(self.node-len(X))
		self.D = {a: i for i,a in enumerate(X)}
		self.lmr = [(0,0,0)]*self.node + [(x,x,x) for x in self.X]
		for i in range(self.node-1, 0, -1):
			self.lmr[i] = (self.lmr[2*i][0], self.lmr[2*i][2], self.lmr[2*i+1][2])
		self.F = [None]*(self.node*2)
		return
	
	def calc(self, f, x):
		return f[0]*x + f[1]
	
	def add_line(self, a, b):
		f = (a, b)
		i = 1
		while 1:
			l,m,r = self.lmr[i]
			g = self.F[i]
			if g is None:
				self.F[i] = f
				return

			flag_l = self.sign(self.calc(g, l), self.calc(f, l))
			flag_r = self.sign(self.calc(g, r), self.calc(f, r))
			
			if flag_l and flag_r:	# 1) 書き換え
				self.F[i] = f
				return
			
			if not(flag_l or flag_r):	# 2) 書き換えなし
				return
			
			# 3) 以下一部書き換え
			if self.sign(self.calc(g, m), self.calc(f, m)):
				self.F[i], f = f, g
				flag_l = not flag_l

			if flag_l:
				i = 2*i
			else:
				i = 2*i+1
		return


	def query(self, x):
		"""
		return max/min{ax+b |i 番目の直線 (a,b)}
		"""

		i = self.D[x] + self.node
		res = self.dat_unit
		# bottom-up
		while i>0:
			if self.F[i]:
				res = self.operate(res, self.calc(self.F[i], x))
			i >>= 1
		return res
