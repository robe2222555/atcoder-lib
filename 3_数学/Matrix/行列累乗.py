# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/Matrix/行列累乗.py
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
