# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/WeightedUF.py
# 参考: https://qiita.com/drken/items/cce6fc5c579051e64fab
# verified by https://atcoder.jp/contests/abc087/tasks/arc090_b
# Weighted Union-find

class WeightedUF():
	# n要素で初期化
	def __init__(self, n):
		self.n = n
		self.par = list(range(n))
		self.rank = [0]*n
		self.group_num = n

		self.diff_weight = [0]*n

	# ノードxが属する集合の根を求める
	def find(self, x):
		if self.par[x] == x:
			return x
		else:
			r = self.find(self.par[x])
			self.diff_weight[x] += self.diff_weight[self.par[x]]
			self.par[x] = r	# 経路圧縮
			return self.par[x]
		
	# ノード x の重みの取得
	def weight(self, x):
		self.find(x)	# 経路圧縮
		return self.diff_weight[x]
	

	def diff(self, x, y):
		return self.weight(y) - self.weight(x)


	# x から w だけ離れた位置に y を付け加える
	# w[y] = w[x] + w
	def unite(self, x, y, w):
		w += self.weight(x)
		w -= self.weight(y)

		x = self.find(x)
		y = self.find(y)
		if x == y:
			return False
		
		if self.rank[x] < self.rank[y]:
			x,y = y,x
			w = -w

		if self.rank[x] == self.rank[y]:
			self.rank[x] += 1

		self.par[y] = x
		self.diff_weight[y] = w
		self.group_num-=1

		return True

	# xとyが同じ集合に属するか否か
	def same(self, x, y):
		return self.find(x) == self.find(y)

	# グループの数を返す
	def group_count(self):
		return self.group_num
