# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/整数/素数関係/約数列挙.py
# 約数列挙

def enumDivisions(n):
	res = []
	for i in range(1, int(pow(n, 0.5))+1):
		if n%i == 0:
			res.append(i)
			if n//i != i:
				res.append(n//i)
	return res
