# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/探索/Euler_tour/Euler_tour_nonrec.py
# 参考: https://qiita.com/Kiri8128/items/2b0023bed9af642c751c
# verified by ABC406F
# オイラーツアーの非再帰実装
# （セグ木と一緒に使いたいとき）
# 頂点番号は 1-indexed (1 ~ N)

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
