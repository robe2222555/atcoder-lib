# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/全域木/prim法.py
# あり本
def LI(): return list(map(int, input().split()))
def II(): return int(input())

""" プリム法
一つの頂点vからなる木Tを考える
ほかの頂点からTに接続している辺のうち,最小のものをTに付け加える
最小のものはheapでとる
O(E*logV)

無向辺のもの
"""
from heapq import *

INF=float("inf")
V, E=LI()
# 始点，終点，コスト
Edge=[LI() for _ in range(E)]
G=[[] for _ in range(V)]


Cost=[[INF]*V for _ in range(V)]
Used=[False]*V
for s,t,c in Edge:
	Cost[s][t]=c
	Cost[t][s]=c

def prim():
	res=0
	# [コスト, 頂点]
	q = [[0,0]]

	while True:
		v=-1    # 次の頂点の暫定的な候補
		MIN=INF

		# xに属さない頂点のうち，xからの辺コストが最小の頂点
		while q:
			c,u=heappop(q)
			if not Used[u] and (v==-1 or c<MIN):
				v=u
				MIN=c
				break
	
		if v==-1:
			break
		Used[v]=True
		res+=c

		for u in range(V):
			if Cost[v][u]!=INF:
				heappush(q, [Cost[v][u], u])

	return res

print(prim())


####################################


######################
#   重み付き無向グラフ　（全部連結している）
#   最小全域木をつくる　辺のコスト和が最小の木
######################

from heapq import *

N=0
START=1

Cost=[[float("inf")]*(N+1) for i in range(N+1)]
Past=[[] for i in range(N+1)]
for _ in range(M): # 無向グラフ
	c,u,v=LI()
	Past[u].append((v,c))
	Past[v].append((u,c))


def prim_heap(START):
	sumcost=0
	q=[]
	Fixed=[False for i in range(N+1)] # ノードが確定したかどうか
	Fixed[START]=True
	cnt=0
	for to,cost in Past[START]:
		heappush(q,(cost,to))

	while q and cnt<N:
		cost_st,st=heappop(q)
		if Fixed[st]:
			continue
		Fixed[st]=True
		cnt+=1
		sumcost+=cost_st

		for to,cost in Past[st]:
			if not Fixed[to]:
				heappush(q,(cost,to))

	return sumcost,Fixed,cnt