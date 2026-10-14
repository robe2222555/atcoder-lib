"""
https://ikatakos.com/pot/programming_algorithm/string_search#z-algorithm

from AtCoder Library (CC0 1.0) : https://github.com/atcoder/ac-library
Python 版: https://github.com/not522/ac-library-python
S[0:]とS[i:]の接頭辞が何個まで共通しているか 最長共通接頭辞数
O(|S|)

abc284f
"""

def z_algorithm(s):

	if isinstance(s, str):
		s = [ord(c) for c in s]

	n = len(s)
	if n == 0:
		return []

	z = [0] * n
	j = 0
	for i in range(1, n):
		z[i] = 0 if j + z[j] <= i else min(j + z[j] - i, z[i - j])
		while i + z[i] < n and s[z[i]] == s[i + z[i]]:
			z[i] += 1
		if j + z[j] < i + z[i]:
			j = i
	z[0] = n

	return z

# 文字列S,T  Sの連続部分文字列にTがあるかどうかを判定
# X := T+"$"+S　の順に連結し，0<=i<|S| -> X[i+|T|+1]=|T|を満たすiに存在する
# ABC430E

def is_substr(S:str, T:str):
	X=T+"$"+S
	Z = z_algorithm(X)

	for i in range(len(S)):
		if i+len(T)+1 >= len(Z):
			break
		if Z[i+len(T)+1]==len(T):
			# S[i:i+len(T)]=T
			return i

	return -1