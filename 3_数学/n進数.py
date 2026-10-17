# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/n進数.py

"""
ABC 404 D
Input:
	num_10 := 10進の整数
	n := int
Output:
	num_n := num_10 を n 進数表記に変換し，リストで返す
"""

def base_n(num_10: int, n: int) -> list[int]:
	num_n = []
	while num_10:
		num_n.append(num_10%n)
		num_10 //= n
	num_n = num_n[::-1]
	return num_n



def convert_n2m(Xn: list[int], n, m):
	"return n 進法の整数 X_n (n 進法で i 桁目が Xn[i]) を m 進法に変換"

	# n -> 10
	n10 = 0
	for x in Xn[::-1]:
		n10 *= n
		n10 += x
	
	# 10 -> m
	Xm = []
	while n10>0:
		Xm.append(n10%m)
		n10 //= m

	if len(Xm)==0:
		Xm.append(0)

	return Xm
