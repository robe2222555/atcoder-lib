"""
	Zobrist Hash
	set ならば，各ハッシュ値の xor を取る
	multiset ならば，各ハッシュ値の和を取る

"""


import random
mod = (1<<61) - 1

N=0
hash = [random.randint(1, mod-1) for i in range(N)]
