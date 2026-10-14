# https://github.com/robe2222555/atcoder-lib/blob/main/1_データ構造/Tree/Trie木.py

from collections import defaultdict
import string
alpha=list(string.ascii_lowercase)


# 文字のエンコードはせず，dictで直接管理
class Trie:
	def __init__(self):
		# 木一つだけなので根を設定
		self.node=1
		self.Chi=[defaultdict(lambda : -1)]     # 節点iの子
		self.Value=["#"]        # 節点iの値
		self.Accept=[False]     # 節点iが単語の終端であるかどうか

	# 文字列wordを追加
	def add_word(self, word):
		pos=0 
		for s in word:
			if self.Chi[pos][s]<0:
				self.Chi.append(defaultdict(lambda : -1))
				self.Value.append(s)
				self.Accept.append(False)
				self.Chi[pos][s]=self.node
				self.node+=1
			
			pos=self.Chi[pos][s]
		
		# 単語の終端を保存
		self.Accept[pos]=True

	# 単語wordが存在するかどうか
	def search(self, word):
		pos=0 
		for s in word:
			pos=self.Chi[pos][s]
			if pos<0:
				return False
		
		# 単語の終端が受理状態かどうかを返す
		return self.Accept[pos]

	# abc287-e
	def LCP(self, words):
		LCP=[0]*len(words)
		Sum=[0]*self.node       # 単語数

		for word in words:
			pos=0
			for s in word:
				pos=self.Chi[pos][s]
				Sum[pos]+=1

		for i, word in enumerate(words):
			pos=0
			for j, s in enumerate(word):
				pos=self.Chi[pos][s]
				
				if Sum[pos]>1:
					LCP[i]=j+1
			
		return LCP