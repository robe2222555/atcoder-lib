"""
verified by. ABC362 G
"""
from atcoder import string

S = input().rstrip()
N=len(S)

SA = string.suffix_array(S)

"""
T 以上の suffix のうち，最小のもの = S[SA[ok]:]
"""
def bisearch(T):
	ng = -1
	ok = len(S)
	M=len(T)

	while ok-ng>1:
		mid = (ng+ok)//2
		pos = SA[mid]
		if T <= S[pos:pos+M]:
			ok = mid
		else:
			ng = mid

	return ok