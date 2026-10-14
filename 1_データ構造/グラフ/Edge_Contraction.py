import sys
input = sys.stdin.readline
def LI(): return list(map(int, input().split()))
def II(): return int(input())

# ABC411F AC済み
def main():
	N,M=LI()
	UV = [LI() for _ in range(M)]
	G=[set() for _ in range(N+1)]
	for u,v in UV:
		G[u].add(v)
		G[v].add(u)
	Q=II()
	X=LI()
	X=list(map(lambda x:x-1, X))

	pieces_at_u = [[i] for i in range(N+1)]
	pos_piece = list(range(N+1))
	ans = M*2
	for i in X:
		u,v = UV[i]

		p_u, p_v = pos_piece[u], pos_piece[v]
		####################
		# 頂点 p_u と 頂点 p_v を両端に持つ辺を縮約
		# ans は辺の総数*2
		
		if p_u == p_v:
			print(ans//2)
			continue

		if len(G[p_u])+len(pieces_at_u[p_u]) < len(G[p_v])+len(pieces_at_u[p_v]):
			u,v = v,u
			p_u,p_v = p_v,p_u
		
		## p_u に p_v を移動させる
		# コマ移動
		for j in pieces_at_u[p_v]:
			pieces_at_u[p_u].append(j)
			pos_piece[j] = p_u
		pieces_at_u[v] = []

		# 辺付け替えと削除
		for j in G[p_v]:
			if not (j in G[p_u]):
				G[p_u].add(j)
				ans += 1
			if not (p_u in G[j]):
				G[j].add(p_u)
				ans += 1

			if p_v in G[j]:
				G[j].remove(p_v)
				ans -= 1

		ans -= len(G[p_v])
		G[p_v].clear()

		if p_v in G[p_u]:	# (p_u, p_v)
			G[p_u].remove(p_v)
			ans -= 1

		if p_u in G[p_u]:	# (p_u, p_u)
			G[p_u].remove(p_u)
			ans -= 1
		########################

		print(ans//2)
		continue

	return




if __name__ == '__main__':
	main()