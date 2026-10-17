# https://github.com/robe2222555/atcoder-lib/blob/main/4_文字列/Aho-Corasick.py
# 参考: https://ikatakos.com/pot/programming_algorithm/string_search

from collections import deque

class AhoCorasick:
	def __init__(self, sigma=26):
		self.goto = [[-1] * sigma]
		self.output = [0]
		self.sigma = sigma


	def add(self, arr, ID):
		v = 0
		for c in arr:
			if self.goto[v][c] == -1:
				self.goto[v][c] = len(self.goto)
				self.goto.append([-1] * self.sigma)
				self.output.append(0)
			v = self.goto[v][c]
		self.output[v] |= 1 << ID

	def build(self):
		fail = [0] * len(self.goto)
		que = deque()
		for i in range(self.sigma):
			if self.goto[0][i] == -1:
				self.goto[0][i] = 0
			else:
				fail[self.goto[0][i]] = 0
				que.append(self.goto[0][i])

		while que:
			v = que.popleft()
			self.output[v] |= self.output[fail[v]]
			for i in range(self.sigma):
				u = self.goto[v][i]
				if u == -1:
					self.goto[v][i] = self.goto[fail[v]][i]
				else:
					fail[u] = self.goto[fail[v]][i]
					que.append(u)

	def solve(self, T: list[int]):
		v = 0
		for s in T:
			v = self.goto[v][s]
			# if (self.output[v]>>ID)&1: S_ID が存在
