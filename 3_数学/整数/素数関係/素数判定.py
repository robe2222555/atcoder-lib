# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/整数/素数関係/素数判定.py
# 一つの値の素数判定

def is_prime(n):
	if n<2:
		return False
	i=2
	while i*i<=n:
		if n%i==0:
			return False
		i+=1
	return True
