# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/全域木/クラスカル法.py
def LI(): return list(map(int, input().split()))
def II(): return int(input())

""" クラスカル法
全ての辺をコスト昇順にみて, 閉路ができなければ追加する
追加する頂点をUnionFindで管理し閉路ができるか判定
最初の辺の昇順ソートが一番計算量が重たく　O(ElogE)

無向辺の閉路検出ー>UnionFind
有向辺の閉路ー>トポロジカルソートでDAGをつくる
"""
class UnionFind():
	# n要素で初期化
	def __init__(self, n):
		self.n = n
		self.par = list(range(n))
		self.rank = [0]*n
		self.group_num = n

	# ノードxが属する集合の根を求める
	def find(self, x):
		if self.par[x] == x:
			return x
		else:
			self.par[x] = self.find(self.par[x])
			return self.par[x]

	# xとyの属する集合を併合
	def unite(self, x, y):
		x = self.find(x)
		y = self.find(y)
		if x == y:
			return
		if self.rank[x] < self.rank[y]:
			self.par[x] = y
		else:
			self.par[y] = x
			if self.rank[x] == self.rank[y]:
				self.rank[x] += 1
		self.group_num-=1

	# xとyが同じ集合に属するか否か
	def same(self, x, y):
		return self.find(x) == self.find(y)

	# グループの数を返す
	def group_count(self):
		return self.group_num


INF=float("inf")
V, E=LI()
# 始点，終点，コスト
Edge=[LI() for _ in range(E)]
Edge=sorted(Edge, key=lambda x:x[2])

# 連結でなければINF
def kruskal():
	UF=UnionFind(V)
	res=0

	for st, to, cost in Edge:
		if not UF.same(st, to):
			UF.unite(st, to)
			res+=cost

	if UF.group_count()==1:
		return res
	else:
		return INF
	return res

print(kruskal())