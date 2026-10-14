# ABC426 E
# 三分探索

def f(a):
	return a*a

def ternary(l, r):
	for i in range(50):
		cl = (l*2 + r)/3
		cr = (l + r*2)/3


		if f(cl) < f(cr):
			r=cr
		else:
			l=cl

	return (l+r)/2