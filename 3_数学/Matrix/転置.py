# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/Matrix/転置.py
# 参考: https://qiita.com/rudorufu1981/items/5341d9603ecb1f9c2e5c

"""
ABC 404 B
Input:
	X := (n, m) 行列	# list の二次元配列
Output:
	res := X を 90度だけ時計回りに回転させた行列

X の行について上下反転させたのち，転置させる

反時計回りの回転もある
"""

def rot(X):
	res=[]
	for x in zip(*X[::-1]):
		res.append(list(x))
	return res
