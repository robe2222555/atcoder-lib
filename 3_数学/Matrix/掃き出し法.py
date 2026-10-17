# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/Matrix/掃き出し法.py
# 典型90 57問目
# m行n列の行列の掃き出し法

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
