# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/整数/gcd/cal_ratio.py

from math import gcd

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
