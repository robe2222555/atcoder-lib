# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/組み合わせ/組み合わせ計算.py

LIM = 1<<20
mod = 998244353
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