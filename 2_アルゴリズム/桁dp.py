# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/桁dp.py

mod = 998244353
def solve(N: int, M):
	N = str(N)
	# 10 進数
	LIM = len(N)
	# N 以下の整数であって，S=0,1,...,M であるものの個数

	eq = 1
	eq_s = 0
	dp = [[0]*(M+1) for _ in range(LIM+1)]
	for i in range(LIM)[::-1]:
		# 未満 <- 等しい
		for j in range(N[i]):
			nx_s = -1
			# nx_s = eq_s + f(j)
			if eq_s<=M and nx_s<=M:
				dp[i][nx_s] = (dp[i][nx_s] + eq)%mod

		# 等しい <- 等しい
		nx_s = -1
		# eq_s = eq_s + f(N[i])
		# もし N[i:] が条件を満たさないならば，eq = 0

		# 未満 <- 未満
		for j in range(M+1):
			for k in range(10):
				nx_s = -1
				# nx_s = j+f(k)
				dp[i][nx_s] += dp[i+1][j]

	ans = dp[0][M] + eq
	return ans