# https://github.com/robe2222555/atcoder-lib/blob/main/4_文字列/文字列の辞書順.py
# ord("A") : Unicodeのコードを返す
# A:65 ~ Z:90   a:97~z:122   26文字


base=ord("A")
def Dictionary(S, mod=1):
	"""
	Sと同じ長さの文字列を辞書順で並べたとき
	S未満の文字列の数
	O(N)   modあり
	"""
	N=len(S)
	cnt=0
	# 26進数
	for i in range(N):
		cnt+=pow(26,N-1-i,mod)*(ord(S[i])-base)
		cnt%=mod
	return cnt

