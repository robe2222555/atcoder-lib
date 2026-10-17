# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/整数/gcd/extgcd.py
# あり本　拡張ユークリッドの互除法
# ax+by=gcd(a,b)の解：(x,y)とd=gcd(a,b)を返す
# ユークリッドの互除法でb=0まで続けて : (a, b) => (b, a%b) => ... => (a, 0)
# (a, b)         : ax  + b              = gcd(a,b)
# (b, a%b)       : bx' + (a-(a//b)*b)y' = ay'+b(x'-(a//b)*y') = gcd(a,b)
#   ：
# (gcd(a, b), 0) : gcd(a,b)*1 + 0       = gcd(a,b)

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
