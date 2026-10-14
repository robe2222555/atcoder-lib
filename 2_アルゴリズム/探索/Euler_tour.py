#######
# オイラーツアーの非再帰実装
# 参考: https://qiita.com/Kiri8128/items/2b0023bed9af642c751c
# ABC406F で動作確認済み（セグ木と一緒に使いたいとき）
################

def Euler_tour(G, N, root = 1):
	pre = [-1]*(N+1)
	post = [-1]*(N+1)
	prepost = []
	traverse = []

	par = [-1]*(N+1)
	stk = [~root, root]
	time = 0
	dep = 0
	while stk:
		u = stk.pop()
		if u>0:
			dep += 1
			pre[u] = time
			prepost.append(u)
			traverse.append(u)

			for v in G[u]:
				if pre[v]>=0: continue	# visitの代わり
				par[v] = u
				stk.append(~v)
				stk.append(v)
		else:
			u = ~u
			post[u] = time
			prepost.append(u)
			traverse.append(par[u])

			dep -= 1

		time += 1
		continue

	return pre, post, par



#########################
# 部分木クエリだけのとき，pre-order のときにのみ tour に入れる
# u の部分木クエリは，[pre[u], post[u])
#

def Euler_tour(N, G, root=1):
	pre = [-1]*(N+1)
	post = [-1]*(N+1)
	par = [-1]*(N+1)
	sz = [1]*(N+1)
	tour = []
	def dfs(u, p=-1):
		pre[u] = len(tour)
		tour.append(u)
		for v in G[u]:
			if v==p: continue
			par[v] = u
			dfs(v, u)
			sz[u] += sz[v]
		post[u] = len(tour)
		return

	dfs(root)
	return pre, post, tour
