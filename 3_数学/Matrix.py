# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/Matrix.py
def LI(): return list(map(int, input().split()))
def II(): return int(input())

######################
# ==行列関係==
# 1. 回転
# 2. 転置
# 3. A^n の繰り返し二乗法
# 4. 掃き出し法
######################






"""
ABC 404 B
Input:
	X := (n, m) 行列	# list の二次元配列
Output:
	res := X を 90度だけ時計回りに回転させた行列

X の行について上下反転させたのち，転置させる
https://qiita.com/rudorufu1981/items/5341d9603ecb1f9c2e5c

反時計回りの回転もある
"""

def rot(X):
	res=[]
	for x in zip(*X[::-1]):
		res.append(list(x))
	return res



######################
"""
行列の転置(listの二次元配列)
"""
def tr(X):
	return list(zip(*X))


################################
# 行列累乗
# abc293e
mod=0

def mat_mul(a, b) :
	I, J, K = len(a), len(b[0]), len(b)
	c = [[0] * J for _ in range(I)]
	for i in range(I) :
		for j in range(J) :
			for k in range(K) :
				c[i][j] += a[i][k] * b[k][j]
				c[i][j] %= mod
	return c


def mat_pow(x, n):
	y = [[0] * len(x) for _ in range(len(x))]

	for i in range(len(x)):
		y[i][i] = 1

	while n > 0:
		if n & 1:
			y = mat_mul(x, y)
		x = mat_mul(x, x)
		n >>= 1

	return y


######################
"""
典型90 57問目
m行n列の行列の掃き出し法
"""

import numpy as np
def sweep_col(N, M, Mat:np.ndarray, is_sweep_row=False):
	m = 0
	for n in range(N):
		# n列目のベクトルを単位ベクトルにする
		vec = Mat[:, n]

		if vec.sum() == 0:
			continue

		if vec[m] == 0:
			for j in range(m+1, M):
				if Mat[j, n] == 1:
					Mat[m] ^= Mat[j]
					break

		if Mat[m ,n] != 1:
			continue

		for j in range(M):
			if j == m:
				continue
			if Mat[j, n] == 1:
				Mat[j] ^= Mat[m]

		if is_sweep_row:
			# n 列目 が単位ベクトル e_m なので，それ以外の列を0にする
			for i in range(n+1, N):
				Mat[m, i] = 0


		m+=1
		if not (m < M):
			break


	return Mat