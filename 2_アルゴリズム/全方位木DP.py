# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/全方位木DP.py

from collections import deque

def re_rooting(G, N, root=1):
	# topological sort
	T=[[] for _ in range(N+1)]
	par = [0]*(N+1)
	order = []
	Depth = [-1]*(N+1)
	Depth[root] = 0
	q = deque([root])
	while len(q) > 0:
		st = q.popleft()
		order.append(st)
		for to in G[st]:
			if Depth[to]<0:
				par[to] = st
				T[st].append(to)
				Depth[to] = Depth[st]+1
				q.append(to)
		continue

	# setting
	unit = (-1, -1)		# (distance, index)
	merge = lambda a, b: a if a>b else b
	adj_bu = lambda a_c, c: (a_c[0]+1, a_c[1])
	adj_td = lambda a_p, p: (a_p[0]+1, a_p[1])

	# bottom up
	dp_bu = [unit for i in range(N+1)]
	for p in order[::-1]:
		if len(T[p])==0:
			dp_bu[p] = (0, p)	# base case
		if len(T[p])>0:
			for c in T[p]:
				dp_bu[p] = merge(dp_bu[p], adj_bu(dp_bu[c], c))

	# top down
	dp_td = [unit for i in range(N+1)]

	for c in T[root]:
		dp_td[c] = (0, root)	# base case

	for p in order:
		ac = unit
		for c in T[p]:
			dp_td[c] = merge(ac, dp_td[c])
			ac = merge(ac, adj_bu(dp_bu[c], c))

		ac = unit
		for c in T[p][::-1]:
			dp_td[c] = merge(dp_td[c], ac)
			ac = merge(adj_bu(dp_bu[c], c), ac)

			if par[p] != 0:
				dp_td[c] = merge(dp_td[c], adj_td(dp_td[p], p))

	for i in range(1, N+1):
		res = merge(dp_bu[i], adj_td(dp_td[i], i))
		print(res[1])

	return