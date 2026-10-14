########################################
# 自作ライブラリより math.gcd の方が早い
#

from math import gcd

# あり本
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


################################################
# 有理数 a/b を規約な分数＝整数のペアで表現

def cal_ratio(a,b):
	g = gcd(a, b)
	a=a//g
	b=b//g
	return (a, b)


# あるいは fractionを使う
from fractions import Fraction as fr
fr(1,3)	# 1/3
fr(2,6)	# 1/3

################################################
# あり本　拡張ユークリッドの互除法
# ax+by=gcd(a,b)の解：(x,y)とd=gcd(a,b)を返す

#
# ユークリッドの互除法でb=0まで続けて : (a, b) => (b, a%b) => ... => (a, 0)
# 
# (a, b)         : ax  + b              = gcd(a,b)
# (b, a%b)       : bx' + (a-(a//b)*b)y' = ay'+b(x'-(a//b)*y') = gcd(a,b)
#   ：
# (gcd(a, b), 0) : gcd(a,b)*1 + 0       = gcd(a,b)
# 

def extgcd(a,b):
	d=a # 互除法の最後にa*1=GCDとなったときのaが記憶される
	if b!=0:
		# d, x=y',  y=x'-a//b*y'
		d,y,x=extgcd(b, a%b)
		y-=(a//b)*x
	else:
		x=1
		y=0
	return d,x,y
#################################################

"""     ピックの定理 : 凸多角形が覆っている格子点の個数
https://drken1215.hatenablog.com/entry/2020/12/13/123900
多角形の面積を S
多角形の内部の格子点の個数を I
多角形の周上の格子点の個数を B
としたとき
	S = I + B/2 - 1
"""
