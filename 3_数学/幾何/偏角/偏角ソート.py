# https://github.com/robe2222555/atcoder-lib/blob/main/3_数学/幾何/偏角/偏角ソート.py
# verified by ABC442 E
# 偏角ソート

from functools import cmp_to_key
def cmp(p1: tuple[int], p2: tuple[int]):
	c1 = (p1[1] > 0) or (p1[1] == 0 and p1[0] > 0)
	c2 = (p2[1] > 0) or (p2[1] == 0 and p2[0] > 0)

	if c1 != c2:
		c = (p1[1] < p2[1]) or (p1[1] == p2[1] and p1[0] < p2[0])
		if c: return 1
		else: return -1

	if p1[0]*p2[1] - p1[1]*p2[0] < 0: return 1
	else: return -1

Cood = [(1,2), (100,20)]
Cood = sorted(Cood, key=cmp_to_key(cmp))
