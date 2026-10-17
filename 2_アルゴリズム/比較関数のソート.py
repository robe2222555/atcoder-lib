# https://github.com/robe2222555/atcoder-lib/blob/main/2_アルゴリズム/比較関数のソート.py

from functools import cmp_to_key
def cmp(x,y):
	"""
	もし x が左に行ってほしいときは 1，右は -1
	等しいなら 0
	usage: A.sort(key=cmp_to_key(cmp))
	"""
	l,r = x[0]*y[1], x[1]*y[0]
	if l<r: return 1
	elif l==r: return 0
	else: return -1