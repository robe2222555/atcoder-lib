# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/整数/素数関係/エラトステネスの篩.py
# エラトステネスの篩 O(n loglog n)

def sieve(n):
	Prime=[1]*(n+1)
	Prime[0]=Prime[1]=0
	for i in range(2, n+1):
		if Prime[i]:
			for j in range(i*2, n+1, i):
				Prime[j]=0
	return Prime
