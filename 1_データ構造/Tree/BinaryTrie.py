# https://ikatakos.com/pot/programming_algorithm/data_structure/trie
# 使ったことない

class BinaryTrie:
	def __init__(self, MAX: int):
		self.root = 0
		self.c0 = [None]
		self.c1 = [None]
		self.cnt = [0]
		self.bit_start = 1<<(MAX.bit_count()-1)

	def cr_node(self):
		self.c0.append(None)
		self.c1.append(None)
		return len(self.c0)-1	# 新しい頂点のラベル

	def add_word(self, word: int):
		pos = 0
		for i in range(self.bit_start, -1, -1):
			if (word>>i)&1:
				if self.c1[pos] is None:
					self.c1[pos] = self.cr_node()
				pos = self.c1[pos]
			else:
				if self.c0[pos] is None:
					self.c0[pos] = self.cr_node()			
				pos = self.c0[pos]



class Rev_BinaryTrie:
	def __init__(self, LEN = -1):
		self.root = 0
		self.c0 = [None]
		self.c1 = [None]
		self.cnt = [0]
		self.LEN = LEN
	

	def cr_node(self):
		self.c0.append(None)
		self.c1.append(None)
		self.cnt.append(0)
		return len(self.c0)-1	# 新しい頂点のラベル

	def add_word(self, word: list[int]):
		# return #(s >= word)
		res = 0
		pos = 0
		self.cnt[0] += 1
		for i in range(self.LEN):
			if word[i]:
				if self.c1[pos] is None:
					self.c1[pos] = self.cr_node()
				pos = self.c1[pos]
			else:
				if not self.c1[pos] is None:
					res += self.cnt[self.c1[pos]]


				if self.c0[pos] is None:
					self.c0[pos] = self.cr_node()			
				pos = self.c0[pos]

			self.cnt[pos] += 1

		res += self.cnt[pos]
		return res

	def delete(self, word: list[int]):
		# assert exist word in Trie
		pos = 0
		self.cnt[0] -= 1
		for i in range(self.LEN):
			if word[i]:
				if self.c1[pos] is None:
					self.c1[pos] = self.cr_node()
				pos = self.c1[pos]
			else:
				if self.c0[pos] is None:
					self.c0[pos] = self.cr_node()			
				pos = self.c0[pos]

			self.cnt[pos] -= 1
		return
