# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/探索/dfs.py
# 再帰はpypyよりpythonのほうが速い


N=0
START=1
G = [[] for _ in range(N+1)]



# ======================
# dfsの "非"再帰実装
# ======================
def dfs_nonrec(root, N, G):
	Visit = [0]*(N+1)

	que = [~root, root]
	while len(que)>0:
		u = que.pop()
		if u>=0:	# 行きがけ順
			Visit[u] = 1

			for v in G[u]:
				if Visit[v]: continue
				que.append(~v)
				que.append(v)

		else:		# 帰りがけ順
			pass
	return


# ======================
# dfsの 再帰実装
# ======================


# calcurate depth
from sys import setrecursionlimit
setrecursionlimit(10**8)
def dfs(root, N, G, Depth=[]):
	if Depth == []:
		Depth=[-1]*(N+1)
		Depth[root]=0

	def _dfs(st):
		for to in G[st]:
			if Depth[to] < 0:
				Depth[to] = Depth[st]+1
				_dfs(to)
		return

	_dfs(root)
	return Depth


# Cnt[v]:=vを根とする部分木のサイズ(自分自身も含む)
from sys import setrecursionlimit
setrecursionlimit(10**8)
def dfs(root, N, G):
	Depth=[-1]*(N+1)
	Depth[root]=0
	Cnt=[0]*(N+1)

	def _dfs(st):
		Cnt[st]+=1
		for to in G[st]:
			if Depth[to] < 0:
				Depth[to] = Depth[st]+1
				_dfs(to)
				Cnt[st] += Cnt[to]
		return
	
	_dfs(root)
	return Depth, Cnt


# Euler Tour
# https://maspypy.com/euler-tour-%E3%81%AE%E3%81%8A%E5%8B%89%E5%BC%B7
def dfs_Etour(root, N, G):
	InOut=[]
	par=[-1 for i in range(N+1)]
	Depth=[-1]*(N+1)

	def _dfs(st):
		InOut.append(st)    # pre-order
		for to in G[st]:
			if Depth[to] < 0:
				Depth[to] = Depth[st] + 1
				par[to] = st
				_dfs(to)
		
		InOut.append(st)    # post-order
		return
	
	Depth[root]=0
	_dfs(root)
	return Depth, InOut





