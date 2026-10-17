# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/整数/gcd/gcd.py
# 参考: あり本
# 自作ライブラリより math.gcd の方が早い

from math import gcd

def gcd(a,b):
	if a<0 or b<0:
		a,b = abs(a), abs(b)

	if a<b:
		return gcd(b, a)
	if b==0:
		return a
	return gcd(b, a%b)
# あり本
# 線分AB上の格子点の個数 = gcd(x2-x1, y2-y1)+1
