# https://github.com/robe2222555/atcoder-lib/blob/main/4_文字列/RollingHash.py
"""
Docstring for lib.3_文字列.RollingHash

文字列の prefix S[1..i] のハッシュ値を求める

verified by ABC141E
"""


class RollingHash:
	def __init__(self, S:str, base:int = 131, mod:int = 10**9+7):
		"""
		h[i] := S[1..i] のハッシュ値
		pw[i] := (base^i)%mod
		"""
		self.n = len(S)
		self.m = mod
		self.b = base
		self.h = [0]*(self.n+1)
		self.pw = [1]*(self.n+1)

		for i in range(1, self.n+1):
			self.h[i] = (self.h[i-1]*base + ord(S[i-1]))%mod
			self.pw[i] = (self.pw[i-1]*base)%mod

		return
	
	def get(self, l, r):
		"return S[l..r] のハッシュ値 (1-based index)"
		return (self.h[r] - self.h[l-1]*self.pw[r-l+1])%self.m