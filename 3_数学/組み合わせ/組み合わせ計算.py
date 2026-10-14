# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/組み合わせ/組み合わせ計算.py

# 高速ver
import math
LIM=1<<20
mod=998244353
binom = [[math.comb(k, i) for i in range(k + 1)] for k in range(11)]


"""
nCk は dp[n][k] 的に求めるか，fact[n]/pow(~~) で求めるかの 2択
modの剰余が欲しい場合，後者はmodが素数でないといけない(フェルマーの小定理)
"""

LIM = 1<<20
fac=[1]*LIM
ninv=[1]*LIM
finv=[1]*LIM
for i in range(2, LIM):
	fac[i] = fac[i-1]*i%mod
	ninv[i] = (-(mod//i)*ninv[mod%i])%mod
	finv[i] = finv[i-1]*ninv[i]%mod

def binom(n,k):
	if n<0 or k<0:
		return 0
	if k>n:
		return 0
	return (fac[n]*finv[k]%mod)*finv[n-k]%mod

def nPk(n,k):
	return fac[n]*finv[n-k]%mod

# n種類から重複を許してk個選ぶ
def nHk(n, k):
	return binom(n+k-1, k)

# nCk(n+k-1, k) = nCk(n+k-1, n-1)


############################
#   modなしver
LIM=0

fact=[1 for i in range(LIM+1)]
for i in range(1,LIM):
	fact[i+1]=(fact[i]*(i+1))

def nCk(n,k):
	return fact[n]//(fact[n-k]*fact[k])

def nPk(n,k):
	return fact[n]//(fact[n-k])

def nHk(n, k):
	return nCk(n+k-1, k)